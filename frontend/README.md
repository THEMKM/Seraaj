# Seraaj Frontend

This directory contains the React frontend for the Seraaj project.

## Development

```bash
npm install
npm run dev
```

The app uses Vite with Tailwind CSS and React Router. Landing page is styled with the brand color scheme and routes to `/dashboard`.

During development, API requests to paths starting with `/api` are proxied to
`http://localhost:8000`. This avoids CORS issues when running the backend and
frontend separately.
