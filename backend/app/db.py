from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./seraaj.db"

engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
