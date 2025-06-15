# Seraaj

This repository contains the source code for **Seraaj**, a volunteer–organization matching platform. It is currently under active development.

## Structure
- `backend/` – FastAPI application
- `frontend/` – React application
- `.github/workflows/` – CI/CD pipelines

### Quick start

```bash
git clone https://github.com/<you>/seraaj.git && cd seraaj

# copy env template
cp .env.example .env

# one-liner dev stack
make dev

# open tabs
open http://localhost:8000/docs        # FastAPI swagger
open http://localhost:5173             # React (start via separate prompt)

# seed demo data if not auto-seeded
make seed

# run all tests
make test
```

The frontend is built with Vite, React Router and Tailwind CSS.

### Authentication

User registration and login are handled by custom JWT endpoints exposed at `/auth/register` and `/auth/login`. A `/auth/users/me` endpoint returns the authenticated user. Tokens are generated with `python-jose`, passwords hashed with `passlib`, and each token encodes the user's role (`VOLUNTEER`, `ORG_ADMIN`, `SUPERADMIN`).

### Seeding demo data

Install backend dependencies then run the seed script to populate the local database with sample data:

```bash
pip install -r backend/requirements.txt
python backend/seed.py
```

The application no longer drops tables automatically on startup. To reset the
database during development you can either run the seed script above or start
the server with `ENV=dev` which calls `init_db()` on launch.

The seed script creates one account for each user role with password `pass123`:

- Volunteer – `volunteer@example.com`
- Organization admin – `orgadmin@example.com`
- Superadmin – `superadmin@example.com`

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

Apply migrations and seed demo data manually if you prefer running the services separately:

```bash
cd backend
alembic upgrade head
python seed.py
uvicorn app.main:app --reload
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The API is now available at `http://localhost:8000/docs` and the web app at
`http://localhost:5173`.

Use the demo credentials above to sign in as each role and explore the platform.

The frontend includes a dark mode toggle in the top-right corner. Your choice is
stored in `localStorage`. Superadmins can visit `/settings` to toggle feature
flags and view basic system health.

### Frontend (React)

```bash
cd frontend         # if you’re running outside docker
npm install
npm run dev         # Vite on :5173

# run lint & e2e tests
npm run lint
npm run test:e2e
```

Design system: Tailwind CSS + shadcn/ui.  Icons: lucide-react.  Charts: recharts.
