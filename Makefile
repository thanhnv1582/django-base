.PHONY: help install run migrate shell test lint format security docker-up docker-down

# ─── Help ────────────────────────────────────────────────────────────────────
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── Setup ───────────────────────────────────────────────────────────────────
install: ## Install dependencies via Poetry + setup pre-commit
	poetry install
	cp -n .env.example .env || true
	poetry run pre-commit install

# ─── Development ─────────────────────────────────────────────────────────────
run: ## Run dev server (port 8000)
	DJANGO_SETTINGS_MODULE=config.settings.dev poetry run python manage.py runserver

shell: ## Open Django shell_plus
	DJANGO_SETTINGS_MODULE=config.settings.dev poetry run python manage.py shell

migrate: ## Run migrations
	DJANGO_SETTINGS_MODULE=config.settings.dev poetry run python manage.py migrate

makemigrations: ## Create new migrations
	DJANGO_SETTINGS_MODULE=config.settings.dev poetry run python manage.py makemigrations

collectstatic: ## Collect static files
	DJANGO_SETTINGS_MODULE=config.settings.prod poetry run python manage.py collectstatic --noinput

createsuperuser: ## Create superuser
	DJANGO_SETTINGS_MODULE=config.settings.dev poetry run python manage.py createsuperuser

# ─── Quality ─────────────────────────────────────────────────────────────────
test: ## Run test suite
	DJANGO_SETTINGS_MODULE=config.settings.test poetry run pytest tests/ -v

test-unit: ## Run unit tests only (no DB)
	DJANGO_SETTINGS_MODULE=config.settings.test poetry run pytest tests/unit/ -v -m unit

test-integration: ## Run integration tests
	DJANGO_SETTINGS_MODULE=config.settings.test poetry run pytest tests/integration/ -v -m integration

test-cov: ## Run tests with HTML coverage report
	DJANGO_SETTINGS_MODULE=config.settings.test poetry run pytest tests/ --cov=src --cov-report=html
	@echo "Coverage report at: htmlcov/index.html"

lint: ## Run ruff linter
	poetry run ruff check src/ tests/

lint-fix: ## Run ruff linter with auto-fix
	poetry run ruff check --fix src/ tests/

format: ## Run black formatter check
	poetry run black --check src/ tests/

format-fix: ## Apply black formatting
	poetry run black src/ tests/

security: ## Run bandit security scan
	poetry run bandit -r src/ -ll -f json -o bandit-report.json; poetry run bandit -r src/ -ll

audit: ## Audit dependencies for vulnerabilities
	poetry run pip-audit

check: lint format security ## Run all quality checks

# ─── Docker ──────────────────────────────────────────────────────────────────
docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start all services
	docker-compose up -d

docker-down: ## Stop all services
	docker-compose down

docker-logs: ## Follow logs for app service
	docker-compose logs -f app

docker-shell: ## Shell into app container
	docker-compose exec app bash

docker-migrate: ## Run migrations inside Docker
	docker-compose exec app python manage.py migrate

docker-createsuperuser: ## Create superuser inside Docker
	docker-compose exec app python manage.py createsuperuser

docker-python: ## Run arbitrary python command inside Docker (e.g. make docker-python CMD="manage.py shell")
	docker-compose exec app python $(CMD)

docker-restart: ## Restart app service
	docker-compose restart app

# ─── Celery ──────────────────────────────────────────────────────────────────
celery-worker: ## Start Celery worker locally
	DJANGO_SETTINGS_MODULE=config.settings.dev poetry run celery -A config.celery worker --loglevel=info

celery-beat: ## Start Celery beat scheduler locally
	DJANGO_SETTINGS_MODULE=config.settings.dev poetry run celery -A config.celery beat --loglevel=info

# ─── Cleanup ─────────────────────────────────────────────────────────────────
clean: ## Remove .pyc files and __pycache__
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null; true
