# Running Seraaj in GitHub Codespaces

Follow these steps to launch the app inside a Codespace.

1. **Create a Codespace** on GitHub and wait for the container to build.
2. In the terminal, copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. **Start the backend and services**:
   ```bash
   make dev
   ```
   This builds the backend and starts Postgres and Redis. The API will be
   available at `http://localhost:${BACKEND_PORT:-8000}`.
4. **Run the frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Vite reads `FRONTEND_PORT` and `VITE_BACKEND_URL` from `.env`. By default the
   frontend runs on `http://localhost:${FRONTEND_PORT:-5173}` and proxies API
   requests to the backend.
5. Open the provided URL in the Codespaces preview or your browser. Log in or
   sign up to explore the demo data.

Stop the stack with `Ctrl+C` in each terminal or `docker compose down`.
