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
