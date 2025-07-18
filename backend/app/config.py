from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # database
    DATABASE_URL: str = "postgresql+psycopg2://seraaj:seraaj@db:5432/seraaj"

    # dev flags
    RESET_ON_START: bool = False        # if True & APP_ENV==local → drop & seed
    SEED_DEMO_DATA: bool = False

    APP_ENV: str = Field("local", pattern="^(local|staging|prod)$")

    class Config:
        env_file = ".env"

_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()  # type: ignore[call-arg]
    return _settings
