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

During development, the port and backend target are read from `.env`. Copy
`../.env.example` to `.env` and adjust `FRONTEND_PORT` and `VITE_BACKEND_URL`
as needed. API requests beginning with `/api` or `/auth` are proxied to
`VITE_BACKEND_URL`.

There is a dark mode toggle in the corner that persists via `localStorage`.
Superadmins can access `/settings` to flip feature flags and check system
health.
