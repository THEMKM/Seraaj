# Backend Development

This directory contains the FastAPI backend and database migrations.

## Migrations

Use [Alembic](https://alembic.sqlalchemy.org/) for schema migrations. The configuration reads the database URL from the `DATABASE_URL` environment variable.

### Create a new migration

```bash
cd backend
alembic revision --autogenerate -m "<message>"
```

### Apply migrations

```bash
alembic upgrade head
```

### Downgrade

```bash
alembic downgrade -1
```
