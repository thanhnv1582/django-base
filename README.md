# Python Seminar — Django Senior: DDD & Clean Architecture

> Production-grade Django application built with **Domain-Driven Design (DDD)** and **Clean Architecture** principles.

---

## 🏗️ Architecture Overview

### 4-Layer Clean Architecture (per domain)

```
apps/{domain}/
├── domain/          Layer 1 — Pure business rules (no Django)
├── application/     Layer 2 — Use Cases, DTOs, Unit of Work
├── infrastructure/  Layer 3 — Django ORM, Repository implementations
└── presentation/    Layer 4 — DRF Views, Serializers, URL routing
```

### Data Flow

```
Request → [Presentation] → DTO → [Application/UseCase]
                                        ↓
                                  [Domain Entity]
                                        ↓
                               [Repository Interface]
                                        ↓
                                 [Infrastructure]
                                  Django ORM Model
                                        ↓
                                  PostgreSQL DB
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- Docker & Docker Compose

### Local Development

```bash
# 1. Clone and install
git clone <repo>
cd python-seminar
make install          # Installs deps + copies .env.example → .env

# 2. Start Database
docker-compose up postgres redis -d

# 3. Run migrations
make migrate

# 4. Start dev server
make run
# → http://localhost:8000

# 5. API Docs
# → http://localhost:8000/api/docs/
# → http://localhost:8000/api/redoc/
```

### Docker (Full Stack)

```bash
make docker-build
make docker-up
# → API:     http://localhost/api/
# → Docs:    http://localhost/api/docs/
# → Flower:  http://localhost:5555
# → Health:  http://localhost/api/health/
```

---

## 📁 Project Structure

```
python-seminar/
├── src/
│   ├── config/              Django project settings (base/dev/prod/test)
│   ├── core/                Shared kernel (exceptions, middleware, base classes)
│   │   ├── base/            BaseEntity, ValueObject, Repository Protocol, UseCase
│   │   ├── exceptions/      AppException hierarchy + global exception handler
│   │   ├── middleware/      RequestId, RequestLogging
│   │   ├── pagination/      StandardResultsPagination
│   │   ├── responses/       Unified success/error response format
│   │   └── health/          Health check endpoint
│   └── apps/
│       └── users/           Example domain (4-layer DDD structure)
├── tests/
│   ├── unit/                Pure Python tests (no DB)
│   ├── integration/         API endpoint tests (SQLite in-memory)
│   └── e2e/                 Full stack tests
├── docker/                  Nginx, Postgres init scripts, entrypoint
├── .github/workflows/       CI pipeline (lint + test + security)
├── Dockerfile               Multi-stage build
├── docker-compose.yml       Full stack: app + postgres + redis + celery + flower + nginx
└── Makefile                 Developer shortcuts
```

---

## 🔧 Development Commands

```bash
make help            # Show all available commands

# ── Development ──────────────────────────────
make run             # Start dev server :8000
make shell           # Django shell
make migrate         # Run migrations
make createsuperuser # Create admin user

# ── Quality ──────────────────────────────────
make lint            # Run ruff linter
make format          # Check black formatting
make security        # Run bandit security scan
make test            # Run all tests
make test-unit       # Unit tests only (fast, no DB)
make test-cov        # Tests + HTML coverage report
make check           # Run ALL quality checks

# ── Docker ───────────────────────────────────
make docker-up       # Start full stack
make docker-down     # Stop all services
make docker-shell    # Shell into app container
make docker-logs     # Follow app logs
```

---

## 🧪 Testing Strategy

| Layer | Type | Tools | Speed |
|-------|------|-------|-------|
| Domain | Unit | pytest (no DB) | ⚡ Very fast |
| Application | Unit (mocked repo) | pytest + MagicMock | ⚡ Fast |
| Infrastructure | Integration | pytest-django + SQLite | 🔶 Medium |
| Presentation | Integration | DRF TestClient | 🔶 Medium |

```bash
# Run only unit tests (no DB — fastest)
pytest tests/unit/ -m unit

# Run integration tests
pytest tests/integration/ -m integration
```

---

## 🌐 API Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| `POST` | `/api/v1/auth/register/` | Public | Register new user |
| `POST` | `/api/v1/auth/login/` | Public | Get JWT tokens |
| `POST` | `/api/v1/auth/token/refresh/` | Public | Refresh JWT |
| `GET` | `/api/v1/users/me/` | Bearer | Get own profile |
| `GET` | `/api/health/` | Public | Health check |
| `GET` | `/api/docs/` | Public | Swagger UI |
| `GET` | `/api/redoc/` | Public | ReDoc |
| `GET` | `/metrics` | Internal | Prometheus metrics |

### Response Format

**Success:**
```json
{
  "success": true,
  "message": "User registered successfully.",
  "data": { "id": "...", "email": "..." },
  "meta": {},
  "request_id": "550e8400-...",
  "timestamp": "2024-01-01T00:00:00+00:00"
}
```

**Error:**
```json
{
  "success": false,
  "error": {
    "code": "EMAIL_ALREADY_REGISTERED",
    "message": "A user with this email already exists.",
    "details": {}
  },
  "request_id": "550e8400-...",
  "timestamp": "2024-01-01T00:00:00+00:00"
}
```

---

## ⚙️ Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `SECRET_KEY` — Django secret key (never hardcode!)
- `DEBUG` — False in production
- `DB_*` — PostgreSQL connection details
- `REDIS_URL` — Redis connection URL
- `SENTRY_DSN` — Error tracking (optional)
- `USE_S3` — Enable S3/MinIO storage (default: False)

---

## 🐳 Services

| Service | Port | Purpose |
|---------|------|---------|
| Nginx | 80, 443 | Reverse proxy + static files |
| Django (Gunicorn) | 8000 (internal) | Application server |
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Cache + Celery broker |
| Celery Worker | — | Background task processing |
| Flower | 5555 | Celery monitoring UI |

---

## 📋 CI/CD Pipeline

On every push/PR:
1. **Lint** — `ruff check` + `black --check`
2. **Security** — `bandit -r src/`
3. **Test** — `pytest --cov --cov-fail-under=70`

Weekly:
4. **Dependency Audit** — `pip-audit` for CVE scanning

---

## 🏛️ Clean Architecture Principles

1. **Dependency Rule**: Dependencies only point inward (Infra → App → Domain)
2. **Domain Purity**: Domain layer has ZERO external framework imports
3. **Business Logic**: Lives ONLY in Use Cases and Domain Entities
4. **Views are thin**: Controllers/Views only handle HTTP plumbing
5. **Serializers are thin**: Only format conversion — no business logic

---

*Built with Python 3.12, Django 5.0, DRF, Poetry, Docker*
