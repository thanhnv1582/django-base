# Task: Django Senior DDD & Clean Architecture

## Phase 1: Foundation
- [x] pyproject.toml (Poetry setup)
- [x] .env.example
- [x] manage.py
- [x] Makefile
- [x] src/config/settings/base.py
- [x] src/config/settings/dev.py
- [x] src/config/settings/prod.py
- [x] src/config/settings/test.py
- [x] src/config/urls.py, wsgi.py, asgi.py, celery.py
- [x] src/core/base/ (entity, value_object, domain_event, repository, use_case, model)
- [x] src/core/exceptions/ (base, handlers)
- [x] src/core/responses/api.py
- [x] src/core/middleware/ (request_id, logging)
- [x] src/core/pagination/standard.py
- [x] .gitignore

## Phase 2: Users Domain
- [x] src/apps/users/domain/ (Entity, VOs Email+FullName, Events, Repository interface)
- [x] src/apps/users/application/ (DTOs, Use Cases: register+get_profile, UoW)
- [x] src/apps/users/infrastructure/ (Django CustomUser Model, DjangoUserRepository)
- [x] src/apps/users/presentation/v1/ (Views, Serializers, URLs)
- [x] src/apps/users/apps.py

## Phase 3: Infrastructure
- [x] Dockerfile (multi-stage: builder + runner)
- [x] docker-compose.yml (6 services)
- [x] docker-compose.override.yml (dev hot-reload)
- [x] docker/nginx/nginx.conf + conf.d/default.conf
- [x] docker/scripts/entrypoint.sh

## Phase 4: Quality & CI/CD
- [x] .github/workflows/ci.yml (lint + security + test)
- [x] .github/workflows/security.yml (weekly pip-audit)
- [x] pytest config in pyproject.toml
- [x] tests/conftest.py (shared fixtures)
- [x] tests/unit/users/test_user_entity.py
- [x] tests/integration/users/test_user_api.py

## Phase 5: Senior Features + README
- [x] Health check endpoint (core/health/views.py + urls.py)
- [x] Prometheus via django-prometheus in settings
- [x] Sentry integration in base.py
- [x] Swagger/Redoc via drf-spectacular in urls.py + settings
- [x] README.md (comprehensive docs)
