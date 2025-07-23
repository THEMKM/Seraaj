# Seraaj Backend

This directory contains the FastAPI backend for the Seraaj project.

## Development

Install dependencies:
```
pip install -r requirements.txt
```

Run the server:
```
uvicorn app.main:app --reload
```

### Migrations

Create the database tables:

```bash
alembic upgrade head
```

Create a new migration after editing models:

```bash
alembic revision --autogenerate -m "describe change"
```

### Matching job

Run Celery with beat to compute match scores daily:

```bash
celery -A app.matching worker -B --loglevel=info
```

### Testing

`make test` automatically runs the suite inside the Docker container when
services are running. If Docker isn't available, tests execute locally
using an SQLite database configured in `backend/tests/conftest.py`.
