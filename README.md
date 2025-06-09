# Seraaj

This repository contains the source code for **Seraaj**, a volunteer–organization matching platform. It is currently under active development.

## Structure
- `backend/` – FastAPI application
- `frontend/` – React application
- `.github/workflows/` – CI/CD pipelines

### Quick start

```bash
cp .env.sample .env  # adjust values as needed
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run backend tests:

```bash
pytest
```

To run the frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend is built with Vite, React Router and Tailwind CSS.

### Environment variables

Copy `.env.sample` to `.env` and review values. At minimum, set `SECRET_KEY` for JWT signing.

### Database migrations

Run Postgres locally via docker compose:

```bash
docker-compose up -d db
```

Apply migrations with Alembic:

```bash
cd backend
alembic upgrade head
```

Generate a new migration after modifying models:

```bash
alembic revision --autogenerate -m "describe change"
```
