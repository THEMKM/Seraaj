# Running Seraaj in GitHub Codespaces

## One-time setup

```bash
# In the Codespace terminal
cp .env.example .env
cp .env.example frontend/.env
```

Start the stack
```bash
# backend + services (runs in watch-mode)
docker compose up --build backend db redis
```
Wait until the Ports panel shows 8000 exposed—that means FastAPI is healthy.

In a second terminal:

```bash
cd frontend
npm install -D @tailwindcss/forms
npm install
npm run dev             # Vite on ${FRONTEND_PORT:-5173}
```

GitHub will prompt to forward ports 5173 and ${BACKEND_PORT}.
Open the 5173 URL and the React app will talk to the API automatically.

Building production assets inside a Codespace
```bash
cd frontend
VITE_BACKEND_URL="$(gp url ${BACKEND_PORT:-8000})" npm run build
```
The gp url command prints the public URL Codespaces assigned to the backend
( e.g. https://8000-coolname.github.dev ).
The generated frontend/dist will now work when served from any static host.
