# 0001: Stack & Folder Layout

Date: 2025-06-09

## Status

Accepted

## Context

This project needs a clear baseline architecture so that multiple agents can scaffold features in a predictable place. The README already defines the technology choices for the MVP, but we need to document them in an ADR and lock in the high level directory layout.

## Decision

We adopt the following stack and repository structure:

- **Backend** – Python 3.12 with **FastAPI** and **SQLModel**. Background jobs run via **Celery** using **Redis** as the broker. Database is **PostgreSQL** and migrations managed by **Alembic**. Source lives in `backend/`.
- **Auth** – handled by **fastapi-users** issuing JWT tokens. Role based access control is VOLUNTEER, ORG_ADMIN and SUPERADMIN.
- **Matching engine** – starts with a `scikit-learn` cosine similarity implementation. When the feature flag `alg_v2` is enabled we will switch to an embeddings based approach.
- **Front-end** – **React** 18 bootstrapped with **Vite** and written in **TypeScript**. Styling uses **Tailwind CSS**. Code lives in `frontend/`.
- **Testing** – unit tests with **pytest**, end-to-end tests with **Playwright**. Coverage target is 90 %.
- **CI/CD** – **GitHub Actions** builds, lints, tests and publishes Docker images. Previews deploy to fly.io and production to render.com.

The top level folders are:

```
backend/    # FastAPI app, models, routers and workers
frontend/   # React application
scripts/    # helper scripts and seed data
infra/      # docker-compose, deploy config
docs/adr/   # this and future architecture decision records
```

## Consequences

All contributors should place new backend code under `backend/` and frontend code under `frontend/`. ADRs live in `docs/adr`. This structure lets automation and CI jobs run in predictable paths and keeps the repository organized as we implement the remaining tasks.
