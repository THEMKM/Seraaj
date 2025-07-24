from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .config import get_settings
from .routers import (
    auth,
    volunteer,
    organization,
    opportunity,
    application,
    application_extra,
    recognition,
    settings as settings_router,
    conversation,
    workspace,
    forum,
    analytics,
)
from .routers import match as match_router
from .db import engine, SQLModel
from seed import seed_demo_data

settings = get_settings()

app = FastAPI(title="Seraaj API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL", "*")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(volunteer)
app.include_router(organization)
app.include_router(opportunity)
app.include_router(application)
app.include_router(application_extra)
app.include_router(recognition)
app.include_router(settings_router)
app.include_router(match_router.router)
app.include_router(conversation)
app.include_router(workspace)
app.include_router(forum)
app.include_router(analytics)


@app.on_event("startup")
def on_startup():
    if settings.RESET_ON_START and settings.APP_ENV == "local":
        SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    if settings.SEED_DEMO_DATA:
        seed_demo_data()


@app.get("/")
def read_root():
    return {"message": "Seraaj API"}


if __name__ == "__main__":
    import uvicorn, os

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=settings.APP_ENV == "local",
    )
