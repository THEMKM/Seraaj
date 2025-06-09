# Seraaj – Volunteer ⇄ Organization Matching Platform

**Version 0.1 (MVP definition)**  
Author: Mohammed Abobakr • Date: 2025-06-09

---

## 🌐 Project Vision
Seraaj (“lantern” in Arabic) is an open-source, AI-assisted platform that removes friction from
volunteer recruitment and recognition.  
* Volunteers maintain **one** rich profile and can **1-click-apply** to any opportunity.  
* Organizations receive an **automatic relevance ranking** of applicants plus instant social-media
  recognition cards.  
* A modular matching engine (TF-IDF → embeddings) lets researchers swap in newer models
  without changing the rest of the stack.

---

## 🛠️ Tech Stack (opinionated defaults)

| Layer | Tech | Notes |
|-------|------|-------|
| Backend | **FastAPI + SQLModel** | Python 3.12 / ASGI served by Uvicorn |
| Auth    | **fastapi-users + JWT** | RBAC: VOLUNTEER · ORG_ADMIN · SUPERADMIN |
| Database | **PostgreSQL 16** | `docker compose up db` for local; RDS in prod |
| Jobs | **Celery + Redis** | Nightly matching recompute |
| Matching | `scikit-learn` cosine baseline → flag-gated OpenAI embeddings |
| Front-end | **React 18 + Vite + TypeScript + Tailwind** | TanStack Query for state |
| CI/CD | **GitHub Actions → fly.io (preview) → render.com (prod)** | PR previews auto-deployed |
| Testing | **pytest** (unit) · **Playwright** (e2e) | 90 %+ coverage target |

---

## ⚡ Quick-start (local)

```bash
git clone https://github.com/<you>/seraaj.git && cd seraaj

# 1. spin up services
docker compose up -d db redis

# 2. backend
cd backend
poetry install
alembic upgrade head
uvicorn app.main:app --reload

# 3. frontend
cd ../frontend
npm i
npm run dev
