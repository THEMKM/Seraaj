from fastapi import FastAPI
import os

from .db import init_db
from .routers import (
    auth,
    volunteer,
    organization,
    opportunity,
    application,
    recognition,
    settings,
)

app = FastAPI(title="Seraaj API")

app.include_router(auth)
app.include_router(volunteer)
app.include_router(organization)
app.include_router(opportunity)
app.include_router(application)
app.include_router(recognition)
app.include_router(settings)


@app.on_event("startup")
def on_startup():
    if os.getenv("ENV") == "dev":
        init_db()


@app.get("/")
def read_root():
    return {"message": "Seraaj API"}
