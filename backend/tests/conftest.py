import os
import subprocess


def _docker_service_running(service: str = "db") -> bool:
    """Return True if the specified docker compose service is running."""
    try:
        result = subprocess.run(
            ["docker", "compose", "ps", "-q", service],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
            text=True,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def pytest_configure(config):
    """Fallback to SQLite when the db service is not available."""
    if not _docker_service_running():
        os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
