from .auth import router as auth
from .volunteer import router as volunteer
from .organization import router as organization
from .opportunity import router as opportunity
from .application import router as application, extra_router as application_extra
from .recognition import router as recognition
from .settings import router as settings
from .match import router as match_router
from .conversation import router as conversation
from .workspace import router as workspace
from .forum import router as forum
from .analytics import router as analytics

__all__ = [
    "auth",
    "volunteer",
    "organization",
    "opportunity",
    "application",
    "application_extra",
    "recognition",
    "settings",
    "match_router",
    "conversation",
    "workspace",
    "forum",
    "analytics",
]
