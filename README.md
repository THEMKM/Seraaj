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

### Seeding demo data

Run the seed script to populate the local database with sample data:

```bash
python backend/seed.py
```

### Environment variables

Copy `.env.sample` to `.env` and review values. At minimum, set `SECRET_KEY` for JWT signing.
Set `REDIS_URL` if you want background jobs to run (defaults to `redis://localhost:6379/0`).

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

### Matching job

Celery runs a nightly task to recompute volunteer–opportunity match scores.
Start a worker with beat enabled:

```bash
celery -A app.matching worker -B --loglevel=info
```

### Recognition service

The `/recognition/{app_id}` endpoint generates a signed Cloudinary upload URL and
returns a PNG link for social media sharing.

### Local deployment

You can try the full stack locally using Docker Compose for Postgres and Redis.

```bash
docker-compose up -d  # starts `db` and `redis` services
```

Apply migrations and seed demo data:

```bash
cd backend
alembic upgrade head
python seed.py  # optional sample data
```

Start the backend and frontend in separate terminals:

```bash
uvicorn app.main:app --reload
```

```bash
cd ../frontend
npm run dev
```

The API is now available at `http://localhost:8000/docs` and the web app at
`http://localhost:5173`.
