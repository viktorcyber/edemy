# Makefile

.PHONY: help setup-hooks watch up down build migrate makemigrations shell test test-e2e lint logs

COMPOSE := docker compose

help:
	@echo "Available commands:"
	@echo "  make setup-hooks   - Enable local Git pre-push checks"
	@echo "  make watch          - Watch for changes and rebuild"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make build          - Rebuild images"
	@echo "  make migrate        - Run database migrations"
	@echo "  make makemigrations - Generate new migrations"
	@echo "  make shell          - Open Django shell"
	@echo "  make test           - Run backend tests"
	@echo "  make test-e2e       - Run Playwright E2E tests"
	@echo "  make lint           - Lint backend + frontend"
	@echo "  make logs           - View server logs"

setup-hooks:
	git config core.hooksPath .githooks

watch:
	$(COMPOSE) watch

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

migrate:
	$(COMPOSE) exec server python manage.py migrate

makemigrations:
	$(COMPOSE) exec server python manage.py makemigrations

shell:
	$(COMPOSE) exec server python manage.py shell

test:
	$(COMPOSE) exec server pytest

test-e2e:
	$(COMPOSE) exec client bunx playwright test

lint:
	$(COMPOSE) exec server ruff check .
	$(COMPOSE) exec client bun run lint

logs:
	$(COMPOSE) logs -f server

notebook:
	source ./.venv/bin/activate && uv run --with jupyter jupyter lab