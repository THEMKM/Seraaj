.PHONY: dev seed test

dev:  ## spin up full stack locally
	docker compose up --build backend db redis

seed: ## run seed script against running backend
	docker compose exec backend python -m app.seed

test: ## run pytest inside backend container
	docker compose exec backend pytest -q
