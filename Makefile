.PHONY: dev seed test

dev:  ## spin up full stack locally
	docker compose up --build backend worker db redis

seed: ## run seed script against running backend
	docker compose exec backend python seed.py

test: ## run pytest; use container when available
	@if docker compose ps -q backend >/dev/null 2>&1; then \
		docker compose exec backend pytest -q; \
	else \
		pytest -q; \
	fi
