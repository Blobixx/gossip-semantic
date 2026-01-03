install:
	uv sync

run:
	uv run uvicorn app.app:app --reload

revision:
	uv run alembic revision --autogenerate -m "auto"

upgrade:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade -1

db-up:
	docker compose up -d

build:
	docker compose build

api:
	docker compose up -d
	docker compose up api

restore:
	docker compose up -d db
	docker compose run --rm restore

run-tests:
	docker compose up -d db
	docker compose run --rm tests

down:
	docker compose down
	
format:
	uv run ruff format