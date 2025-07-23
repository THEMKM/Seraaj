from __future__ import annotations
import os
from celery import Celery
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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
        for app in applications:
            vol = session.get(VolunteerProfile, app.volunteer_id)
            opp = session.get(Opportunity, app.opportunity_id)
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
                vol_text = " ".join((vol.skills or []) + (vol.interests or []))
                opp_text = " ".join(opp.skills_required or [])
                vectorizer = TfidfVectorizer()
                vec = vectorizer.fit_transform([vol_text, opp_text])
                score = cosine_similarity(vec[0], vec[1])[0][0]
            app.match_score = float(score)
            session.add(app)
        session.commit()
        return len(applications)


celery_app.conf.beat_schedule = {
    "nightly-match": {
        "task": "matching.compute_match_scores",
        "schedule": 24 * 60 * 60,  # once a day
    }
}
