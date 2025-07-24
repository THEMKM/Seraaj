from __future__ import annotations

import os

import numpy as np
from celery import Celery
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlmodel import Session, select

from .db import engine
from .models import Application, VolunteerProfile, Opportunity
from .routers.settings import FLAGS

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("matching", broker=REDIS_URL)


@celery_app.task
def compute_match_scores() -> int:
    """Compute and persist match scores for all applications."""
    with Session(engine) as session:
        applications = session.exec(select(Application)).all()
        if not applications:
            return 0

        vol_ids = {a.volunteer_id for a in applications}
        opp_ids = {a.opportunity_id for a in applications}
        volunteers = {
            v.user_id: v
            for v in session.exec(
                select(VolunteerProfile).where(VolunteerProfile.user_id.in_(vol_ids))
            )
        }
        opportunities = {
            o.id: o
            for o in session.exec(
                select(Opportunity).where(Opportunity.id.in_(opp_ids))
            )
        }

        updated = 0

        if FLAGS.get("alg_v2"):
            vol_vecs: dict[str, np.ndarray] = {}
            opp_vecs: dict[str, np.ndarray] = {}
        else:
            texts = [
                " ".join((vol.skills or []) + (vol.interests or []))
                for vol in volunteers.values()
            ] + [" ".join(opp.skills_required or []) for opp in opportunities.values()]
            vectorizer = TfidfVectorizer()
            vectorizer.fit(texts)
            vol_vecs = {
                vid: vectorizer.transform(
                    [
                        " ".join(
                            (volunteers[vid].skills or [])
                            + (volunteers[vid].interests or [])
                        )
                    ]
                )
                for vid in volunteers
            }
            opp_vecs = {
                oid: vectorizer.transform(
                    [" ".join(opportunities[oid].skills_required or [])]
                )
                for oid in opportunities
            }

        for app in applications:
            vol = volunteers.get(app.volunteer_id)
            opp = opportunities.get(app.opportunity_id)
            if not vol or not opp:
                continue
            if FLAGS.get("alg_v2"):
                if vol.embedding is None or opp.embedding is None:
                    score = 0.0
                else:
                    v = np.array(vol.embedding)
                    o = np.array(opp.embedding)
                    score = float(v @ o / (np.linalg.norm(v) * np.linalg.norm(o)))
            else:
                vol_vec = vol_vecs[app.volunteer_id]
                opp_vec = opp_vecs[app.opportunity_id]
                score = cosine_similarity(vol_vec, opp_vec)[0][0]
            app.match_score = float(score)
            session.add(app)
            updated += 1

        session.commit()
        return updated


celery_app.conf.beat_schedule = {
    "nightly-match": {
        "task": "matching.compute_match_scores",
        "schedule": 24 * 60 * 60,  # once a day
    }
}
