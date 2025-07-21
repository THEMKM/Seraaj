# Seraaj Frontend

This directory contains the React frontend for the Seraaj project.

## Development

```bash
npm install
npm run dev
```

The app uses Vite with Tailwind CSS and React Router. Available routes include:

- `/` – Landing page with hero and feature list.
- `/signup` and `/login` – Auth forms with email/password and Google button.
- `/dashboard` – Volunteer dashboard listing recommended opportunities.
- `/opportunities` – Opportunity search.
- `/opportunity/:id` – Detail page.

During development, API requests to paths starting with `/api` are proxied to
`http://localhost:8000`. This avoids CORS issues when running the backend and
frontend separately.

There is a dark mode toggle in the corner that persists via `localStorage`.
Superadmins can access `/settings` to flip feature flags and check system
health.
