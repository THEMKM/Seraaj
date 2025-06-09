from fastapi import FastAPI

from .db import init_db
from .routers import auth, volunteer, organization, opportunity, application, recognition

app = FastAPI(title="Seraaj API")

app.include_router(auth)
app.include_router(volunteer)
app.include_router(organization)
app.include_router(opportunity)
app.include_router(application)
app.include_router(recognition)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {"message": "Seraaj API"}
