# ADR 0001: Stack & Folder Layout

## Status
Accepted

## Context
The Seraaj project needs a clear technology stack and directory structure so contributors can quickly understand how the system fits together. We want an opinionated yet flexible layout that supports FastAPI, React, and container-based deployments.

## Decision
- **Backend** uses **FastAPI 0.110** with **SQLModel** for ORM, served by **Uvicorn**. Database migrations run via **Alembic** against **Postgres**.
- **Authentication** is handled in-house using **python-jose** to issue JWT tokens. Passwords are hashed with **passlib**, and tokens encode the user role (`VOLUNTEER`, `ORG_ADMIN`, `SUPERADMIN`).
- **Matching** jobs run with **Celery** and **Redis**.
- **Frontend** is a **React 18** application bootstrapped with **Vite** and styled using **Tailwind CSS**. State is managed through **TanStack Query**.
- **Repository layout**
  - `backend/` – FastAPI app (`app/`), Alembic migrations, tests
  - `frontend/` – React source and tests
  - `docs/adr/` – Architecture Decision Records
  - `.github/workflows/` – CI/CD pipelines
  - `docker-compose.yml` – local Postgres & Redis services

## Consequences
- Contributors know where API, frontend, and infrastructure code live.
- CI can target backend and frontend separately while sharing the same repository.
- Future ADRs will build on this folder structure.
