# AGENTS – Codex Coordination Protocol for Seraaj

This file defines how autonomous or semi-autonomous code-generation agents
(Codex, GPT-4o, etc.) collaborate on the codebase.  
Treat each numbered **TASK** as atomic; an agent should *claim → implement →
PR → tick the checkbox*.

---

## 🕹️ Roles

| Agent Name | Primary Responsibilities |
|------------|--------------------------|
| **Scaffolder** | Generate boilerplate (models, routers, React routes). |
| **Implementer** | Flesh out business logic & UI components. |
| **Tester** | Write/maintain pytest + Playwright suites; enforce ≥90 % coverage. |
| **Doc-smith** | Keep `README.md`, ADRs (`/docs/adr/XXXX-*`), OpenAPI schema up-to-date. |
| **Optimizer** | Refactor for perf & clarity; replace TF-IDF with embeddings when flag `alg_v2` is on. |

*An agent may hold multiple roles, but PRs should be role-scoped.*

---

## 🔄 Interaction Contract

1. **SYNC:** Before starting, run `git pull --rebase` to avoid drift.  
2. **TASK PICK:** Open `AGENTS.md`; pick the next unchecked task.  
3. **BRANCH:** `git checkout -b <task-id>/<short-desc>`  
4. **DEV:** Implement; commit early & often (`conventional-commit` style).  
5. **TEST:** `make test` must be green locally.  
6. **PR:** Push & open a Draft PR referencing the task-id.  
7. **REVIEW:** Another agent (or human) reviews & merges when CI passes.  
8. **TICK:** In this doc, tick `[x]` for the task.

---

## 📋 Task List (MVP)

- [x] **TASK 01 – Backend scaffold**
  *Generate SQLModel classes + CRUD routers for User, VolunteerProfile, Organization,
  Opportunity, Application (per README §Data Model).*.

- [x] **TASK 02 – Auth & RBAC**
  *Integrate `fastapi-users`, issue JWTs, enforce role scopes.*

- [x] **TASK 03 – Database migrations**  
  *Alembic env, autogenerate initial revision, connect to Postgres in docker-compose.*

- [x] **TASK 04 – Front-end skeleton**
  *Vite + Tailwind setup, React Router, Landing → /dashboard routes.*

- [x] **TASK 05 – Secure API proxy**
  *`vite.config.ts` devProxy `/api/*` → `http://localhost:8000`.*

- [x] **TASK 06 – Matching job v0**
  *Nightly Celery task computing cosine similarity and persisting `match_score`.*

- [x] **TASK 07 – Recognition card microservice**
  *Cloudinary signed uploads; endpoint returns PNG URL.*

- [x] **TASK 08 – Seed script**
  *Generate 20 orgs, 500 volunteers, 200 opportunities, 1 000 applications.*

- [x] **TASK 09 – Unit tests coverage ≥90 %**
  *Write tests per router & model methods.*

- [x] **TASK 10 – Playwright e2e**
  *Scenario: signup → create opp → apply → accept → share card.*

- [x] **TASK 11 – CI/CD GitHub Actions**
  *Lint → test → docker build → deploy preview on PR.*

- [x] **TASK 12 – Docs & ADR zero**
  *Write Architecture Decision Record 0001: “Stack & Folder Layout”.*

---

## 🧑‍💻 Coding Conventions

* **Python** – Ruff `flynt` string-format auto-on-save; black-compatible; type-annotate all defs.  
* **TS/JS** – ESLint airbnb-typescript; **no** `any`.  
* **Commits** – `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, etc.  
* **Env** – No secrets in repo; use `.env.sample` + GitHub Secrets.

---

## 🛑 Guardrails

* **Fail Fast** – raise `HTTPException` with clear messages.  
* **Test First** – Don’t merge code lacking tests.  
* **Performance Budget** – API < 100 ms p99 local; React bundle ≤ 250 kB gzip.  
* **Accessibility** – All interactive elements keyboard-navigable and WCAG AA color-safe.

---

Happy hacking! 🚀

## 🚀 UI Task List (Phase 2)

The following tasks expand the front-end according to the "Seraaj Front-End Spec & User Stories" document. Implement them sequentially, following the interaction contract above. Each task should be completed in its own branch and accompanied by unit/e2e tests and documentation updates where noted.

- [x] **UI01 – Landing Page**
  *Implement `/` with hero header, feature blocks and footer.*  
  *CTA buttons route to `/signup` and `/login`.*  
  *Ensure mobile and desktop layouts with Tailwind; add accessibility labels.*

- [x] **UI02 – Auth Pages**
  *Create `/signup` and `/login` pages with email & password fields, Google auth button, and form validation.*  
  *After success redirect to `/dashboard`.*  
  *Write e2e test covering signup and login flow.*

- [x] **UI03 – Volunteer Dashboard**
  *Show profile completion meter and recommended opportunities.*  
  *List recent applications in a table.*  
  *Integrate TanStack Query for API calls.*

- [x] **UI04 – Opportunities List**
  *Implement filters (keywords, skills multiselect, location autocomplete, remote toggle) and sorting.*  
  *Display results using `OpportunityCard` component; show empty and error states.*

- [x] **UI05 – Opportunity Detail**
  *Create detail view with apply button, markdown description, and organization sidebar.*  
  *Sticky Apply button on mobile.*

- [x] **UI06 – Org Admin Dashboard**
  *Show stats widgets and opportunities table with bulk actions.*  
  *Add link to create new opportunity.*

- [x] **UI07 – Opportunity Form**
  *Page for create/edit opportunity with validation (title ≥5 chars, description ≥20, dates logic).*  
  *Save draft and publish flows, redirect back with toast.*

- [x] **UI08 – Applicant Review**
  *Tabbed view of applicants sorted by match score.*  
  *Accept/Decline actions with undo snackbar.*  
  *"Share Recognition" modal with preview and share buttons.*

- [ ] **UI09 – Superadmin Settings**  
  *Toggle feature flags and show system health chips.*  
  *Refresh button fetches latest status.*

- [x] **UI10 – Reusable Components**
  *Build `OpportunityCard`, `ProfileCompletionMeter`, `DataTable`, `Modal`, `Snackbar`, and `FormField` as described.*

- [ ] **UI11 – Theme & Dark Mode**  
  *Configure Tailwind for primary/secondary colors, rounded corners and shadows.*  
  *Add dark mode toggle stored in localStorage.*

- [ ] **UI12 – Animations & A11y**  
  *Use Framer Motion for card entry, modals, and snackbars.*  
  *Ensure all interactive elements are keyboard navigable and have ARIA labels.*

- [ ] **UI13 – Frontend Tests**  
  *Expand Playwright tests to cover signup-apply-accept flow and common error cases.*  
  *Add React Testing Library unit tests for critical components.*

