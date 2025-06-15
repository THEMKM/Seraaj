from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
from pgvector.sqlalchemy import Vector

from .config import get_settings

settings = get_settings()
connect_args = {
    "check_same_thread": False
} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(
    settings.DATABASE_URL, echo=False, pool_pre_ping=True, connect_args=connect_args
)

# ensure pgvector extension exists (Postgres only)
if engine.url.get_backend_name() == "postgresql":
    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector")


def init_db() -> None:
    """Reset and initialize the database tables."""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
