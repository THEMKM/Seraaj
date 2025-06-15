from fastapi import APIRouter, Depends
try:
    from sse_starlette.sse import EventSourceResponse  # type: ignore
except Exception:  # pragma: no cover - fall back for tests
    from fastapi.responses import Response as EventSourceResponse
from sqlmodel import select

from ..db import get_session
from ..models import Opportunity, VolunteerProfile
from ..services.embedding import embed
from .dependencies import get_current_user

router = APIRouter(prefix="/match", tags=["match"])


def rank(vol_embedding: list[float], opps: list[Opportunity]):
    """Cosine-similarity ranking (quick numpy implementation)."""
    import numpy as np

    v = np.array(vol_embedding)
    for o in opps:
        if o.embedding:
            o._score = float(
                v @ np.array(o.embedding) / (np.linalg.norm(v) * np.linalg.norm(o.embedding))
            )
        else:
            o._score = -1.0
    return sorted(opps, key=lambda o: o._score, reverse=True)


@router.get("/me")
def stream_my_matches(current=Depends(get_current_user), session=Depends(get_session)):
    vp = session.get(VolunteerProfile, current.id)
    if not vp or not vp.embedding:
        return []
    opps = session.exec(select(Opportunity)).all()
    ranked = rank(vp.embedding, opps)[:20]

    async def event_generator():
        for o in ranked:
            yield f"data: {o.id}|{o.title}|{o._score}\n\n"

    return EventSourceResponse(event_generator())
