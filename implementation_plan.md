# Django Senior — DDD & Clean Architecture Blueprint

Dự án Django production-grade từ đầu, áp dụng **Domain-Driven Design (DDD)** và **Clean Architecture** với 4 lớp nghiêm ngặt tại từng app, tích hợp đầy đủ Docker, CI/CD, observability, và các tính năng Senior-level.

---

## 📋 Luồng Dữ liệu (Data Flow)

```
HTTP Request
     │
     ▼
┌──────────────────────────────────┐
│  PRESENTATION LAYER              │
│  (apps/{domain}/presentation/)   │
│  ┌───────────────────────────┐   │
│  │  DRF ViewSet / APIView    │   │  ← Chỉ nhận request, gọi Use Case
│  │  Serializer (I/O convert) │   │  ← Chỉ validate format, không có logic
│  │  URL Router (v1/v2)       │   │
│  └───────────────────────────┘   │
└────────────────┬─────────────────┘
                 │ DTO Input
                 ▼
┌──────────────────────────────────┐
│  APPLICATION LAYER               │
│  (apps/{domain}/application/)    │
│  ┌───────────────────────────┐   │
│  │  Use Cases / Services     │   │  ← Toàn bộ business logic ở đây
│  │  Input/Output DTOs        │   │  ← Pydantic dataclasses
│  │  Unit of Work             │   │  ← Quản lý transaction boundary
│  └───────────────────────────┘   │
└────────────────┬─────────────────┘
                 │ Domain Object / Commands
                 ▼
┌──────────────────────────────────┐
│  DOMAIN LAYER                    │
│  (apps/{domain}/domain/)         │
│  ┌───────────────────────────┐   │
│  │  Entities (Pure Python)   │   │  ← Không import Django
│  │  Value Objects            │   │  ← Immutable
│  │  Domain Events            │   │  ← Raised by Entities
│  │  Repository Interfaces    │   │  ← Abstract Protocol classes
│  └───────────────────────────┘   │
└────────────────┬─────────────────┘
                 │ Repository Interface
                 ▼
┌──────────────────────────────────┐
│  INFRASTRUCTURE LAYER            │
│  (apps/{domain}/infrastructure/) │
│  ┌───────────────────────────┐   │
│  │  Django ORM Models        │   │  ← Persistence models
│  │  Repository Implementations│  │  ← Implements Domain interfaces
│  │  External Services        │   │  ← AWS S3, Email, SMS...
│  │  Migrations               │   │
│  └───────────────────────────┘   │
└──────────────────────────────────┘
```

**Nguyên tắc then chốt:**
- **Domain layer** không biết gì về Django, DRF, hay database
- **Application layer** chỉ biết về Domain, không biết về Django ORM
- **Presentation layer** không chứa business logic — chỉ serialize/deserialize
- **Infrastructure layer** là adapter duy nhất kết nối domain với thế giới bên ngoài
- **Dependency rule**: chỉ một chiều vào trong (Infra → App → Domain)

---

## 📁 Cấu Trúc Files & Folders

```
python-seminar/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # CI pipeline chính
│       └── security.yml              # Bandit security scan
│
├── docker/
│   ├── nginx/
│   │   ├── nginx.conf                # Nginx config chính
│   │   └── conf.d/
│   │       └── default.conf          # Virtual host config
│   ├── postgres/
│   │   └── init.sql                  # DB initialization
│   └── scripts/
│       ├── entrypoint.sh             # Docker entrypoint
│       └── wait-for-it.sh            # Service health check
│
├── src/                              # *** Source code root ***
│   ├── config/                       # Project-level config (thay manage.py root)
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # Shared settings
│   │   │   ├── dev.py                # Development overrides
│   │   │   ├── prod.py               # Production overrides
│   │   │   └── test.py               # Test overrides
│   │   ├── urls.py                   # Root URL config
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── core/                         # *** Shared kernel (không phụ thuộc app) ***
│   │   ├── __init__.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # AppException base class
│   │   │   └── handlers.py           # Global exception handler → JSON format
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── request_id.py         # Inject X-Request-ID header
│   │   │   └── logging.py            # Structured request logging
│   │   ├── pagination/
│   │   │   └── standard.py           # Unified pagination response
│   │   ├── permissions/
│   │   │   └── base.py               # Base permission classes
│   │   ├── responses/
│   │   │   └── api.py                # Unified API response format
│   │   ├── utils/
│   │   │   ├── crypto.py             # Hashing, token generation
│   │   │   ├── datetime_utils.py
│   │   │   └── validators.py
│   │   └── base/
│   │       ├── entity.py             # Base Entity class (id, created_at...)
│   │       ├── value_object.py       # Base Value Object (frozen dataclass)
│   │       ├── domain_event.py       # Base Domain Event
│   │       ├── repository.py         # Abstract Repository Protocol[T]
│   │       ├── use_case.py           # Abstract UseCase[Input, Output]
│   │       └── model.py              # SoftDeleteModel, TimestampedModel
│   │
│   ├── apps/                         # *** Business domains ***
│   │   ├── __init__.py
│   │   │
│   │   └── users/                    # Ví dụ: Users domain
│   │       ├── __init__.py
│   │       │
│   │       ├── domain/               # *** LAYER 1: Pure business rules ***
│   │       │   ├── __init__.py
│   │       │   ├── entities/
│   │       │   │   ├── __init__.py
│   │       │   │   └── user.py       # User Entity (Python class, no Django)
│   │       │   ├── value_objects/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── email.py      # Email VO (validate format)
│   │       │   │   └── password.py   # Password VO (hashing policy)
│   │       │   ├── events/
│   │       │   │   ├── __init__.py
│   │       │   │   └── user_registered.py  # UserRegistered domain event
│   │       │   └── repositories/
│   │       │       ├── __init__.py
│   │       │       └── user_repository.py  # Protocol/ABC interface
│   │       │
│   │       ├── application/          # *** LAYER 2: Orchestrates use cases ***
│   │       │   ├── __init__.py
│   │       │   ├── dtos/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── inputs.py     # RegisterUserInput, LoginInput...
│   │       │   │   └── outputs.py    # UserOutput, TokenOutput...
│   │       │   ├── use_cases/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── register_user.py      # RegisterUserUseCase
│   │       │   │   ├── authenticate_user.py  # AuthenticateUserUseCase
│   │       │   │   └── update_profile.py     # UpdateProfileUseCase
│   │       │   └── services/
│   │       │       └── unit_of_work.py       # UoW wraps transaction scope
│   │       │
│   │       ├── infrastructure/       # *** LAYER 3: Adapters to outside world ***
│   │       │   ├── __init__.py
│   │       │   ├── models/
│   │       │   │   └── user_model.py         # Django ORM Model
│   │       │   ├── repositories/
│   │       │   │   └── django_user_repository.py  # Implements UserRepository
│   │       │   ├── external/
│   │       │   │   └── email_service.py      # SMTP / SendGrid
│   │       │   └── migrations/               # Django migrations
│   │       │       └── 0001_initial.py
│   │       │
│   │       └── presentation/         # *** LAYER 4: HTTP interface ***
│   │           ├── __init__.py
│   │           ├── v1/
│   │           │   ├── __init__.py
│   │           │   ├── views.py      # APIView / ViewSet
│   │           │   ├── serializers.py # Input validation + output format
│   │           │   └── urls.py       # URL routing cho v1
│   │           └── v2/               # (sẵn sàng cho versioning)
│   │               └── __init__.py
│   │
├── tests/                            # *** Test suite ***
│   ├── conftest.py                   # Fixtures, DB setup
│   ├── unit/
│   │   └── users/
│   │       ├── domain/               # Test entities & VOs thuần Python
│   │       └── application/          # Test use cases với mocked repos
│   ├── integration/
│   │   └── users/
│   │       └── test_user_api.py      # Test DRF endpoints
│   └── e2e/
│       └── test_health.py
│
├── Dockerfile                        # Multi-stage build
├── docker-compose.yml                # Full stack: app + db + cache + worker
├── docker-compose.override.yml       # Dev overrides
├── pyproject.toml                    # Poetry + ruff + black + pytest config
├── poetry.lock
├── .env.example                      # Template, không commit .env thật
├── .env                              # (gitignored)
├── manage.py                         # Django manage entry point
├── Makefile                          # Dev shortcuts
└── README.md
```

---

## 🔧 Proposed Changes

### Core Package (`src/core/`)

#### [NEW] `src/core/exceptions/base.py`
Định nghĩa class hierarchy ngoại lệ:
- `AppException(Exception)` — base với `code`, `message`, `status_code`
- `ValidationException`, `NotFoundException`, `AuthException`, `PermissionException`, `ConflictException`

#### [NEW] `src/core/exceptions/handlers.py`
Global DRF exception handler trả về JSON chuẩn:
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "...",
    "details": {}
  },
  "meta": { "request_id": "...", "timestamp": "..." }
}
```

#### [NEW] `src/core/responses/api.py`
Unified success response:
```json
{
  "success": true,
  "data": {},
  "meta": { "page": 1, "total": 100 }
}
```

#### [NEW] `src/core/base/entity.py`
```python
@dataclass
class BaseEntity:
    id: UUID
    created_at: datetime
    updated_at: datetime
    _events: list[DomainEvent] = field(default_factory=list)

    def add_event(self, event): ...
    def pull_events(self): ...
```

#### [NEW] `src/core/base/model.py`
- `TimestampedModel` — abstract Django model với created_at, updated_at
- `SoftDeleteModel` — thêm deleted_at, is_deleted; override delete()

---

### Config (`src/config/settings/`)

#### [NEW] `base.py`
- django-environ cho tất cả secrets
- REST_FRAMEWORK config: JWT auth, throttling mặc định
- CORS, CSRF, Security headers
- Celery config (broker Redis)
- Sentry DSN
- Swagger/Redoc (drf-spectacular)
- Prometheus (django-prometheus)

#### [NEW] `dev.py` / `prod.py` / `test.py`
- Split theo môi trường, override từ base
- Prod: HTTPS redirect, HSTS, secure cookies, Whitenoise

---

### Docker Infrastructure

#### [NEW] `Dockerfile` — Multi-stage
```
Stage 1: builder — cài dependencies via Poetry
Stage 2: runner  — copy chỉ virtualenv, non-root user, tối ưu size
```

#### [NEW] `docker-compose.yml`
| Service | Image | Purpose |
|---------|-------|---------|
| `app` | Custom Django | Gunicorn/WSGI |
| `postgres` | postgres:16-alpine | Primary DB |
| `redis` | redis:7-alpine | Cache + Celery broker |
| `celery` | (same as app) | Background workers |
| `flower` | mher/flower | Celery monitor |
| `nginx` | nginx:alpine | Reverse proxy + static |

#### [NEW] `docker/nginx/nginx.conf`
- Serve `/static/` và `/media/` trực tiếp
- Proxy `location /` đến Gunicorn
- Gzip compression, browser caching headers

---

### CI/CD (`.github/workflows/`)

#### [NEW] `ci.yml`
```yaml
jobs:
  lint:    ruff check + black --check
  test:    pytest --cov --cov-fail-under=80
  security: bandit -r src/
```

#### [NEW] `security.yml`
- Chạy `pip-audit` kiểm tra vulnerable dependencies
- Weekly schedule scan

---

### `pyproject.toml` (Poetry)

**Core dependencies:**
- `django>=5.0`, `djangorestframework`, `django-environ`
- `djangorestframework-simplejwt`, `drf-spectacular`
- `psycopg2-binary`, `django-redis`, `celery`
- `sentry-sdk`, `django-prometheus`, `django-cors-headers`
- `whitenoise`, `gunicorn`

**Dev dependencies:**
- `pytest-django`, `pytest-cov`, `factory-boy`, `faker`
- `ruff`, `black`, `bandit`, `pre-commit`

---

### Users Domain (Ví dụ minh họa đầy đủ)

#### [NEW] `src/apps/users/domain/entities/user.py`
```python
@dataclass
class UserEntity(BaseEntity):
    email: Email        # Value Object
    username: str
    is_active: bool = True

    def deactivate(self):
        self.is_active = False
        self.add_event(UserDeactivated(user_id=self.id))
```

#### [NEW] `src/apps/users/domain/repositories/user_repository.py`
```python
class UserRepository(Protocol):
    def find_by_id(self, id: UUID) -> Optional[UserEntity]: ...
    def find_by_email(self, email: str) -> Optional[UserEntity]: ...
    def save(self, user: UserEntity) -> UserEntity: ...
    def delete(self, id: UUID) -> None: ...
```

#### [NEW] `src/apps/users/application/use_cases/register_user.py`
```python
class RegisterUserUseCase(UseCase[RegisterUserInput, UserOutput]):
    def __init__(self, repo: UserRepository, uow: UnitOfWork): ...
    def execute(self, input: RegisterUserInput) -> UserOutput:
        # 1. Validate business rules
        # 2. Create domain entity
        # 3. Persist via repo
        # 4. Publish domain events
        # 5. Return output DTO
```

---

## ✅ Senior-Level Features

| Feature | Implementation |
|---------|---------------|
| **Soft Delete** | `SoftDeleteModel` override `.delete()` → set `deleted_at`, custom Manager exclude deleted |
| **Health Check** | `GET /api/health/` → check DB ping, Redis ping, return JSON status |
| **Rate Limiting** | DRF throttling: `AnonRateThrottle` (100/day), `UserRateThrottle` (1000/hour) |
| **CORS/CSRF** | `django-cors-headers` CORS config + DRF CSRF enforce |
| **Swagger/Redoc** | `drf-spectacular` tự động generate từ ViewSets, serve tại `/api/docs/` |
| **Sentry** | DSN từ env, capture exceptions + performance traces |
| **Prometheus** | `django-prometheus` expose `/metrics` cho Grafana |
| **Request ID** | Middleware inject `X-Request-ID` header vào mỗi request/response |
| **Structured Logging** | `structlog` log dạng JSON với request_id, user_id |

---

## ⚠️ User Review Required

> [!IMPORTANT]
> **Tên app mẫu**: Kế hoạch sẽ tạo domain `users` làm ví dụ minh họa đầy đủ 4 lớp. Bạn có muốn thêm domain nào khác ngay từ đầu không? (vd: `products`, `orders`, `notifications`)

> [!WARNING]
> **Storage Production**: Cấu hình nginx hiện serve media files local. Nếu triển khai production trên nhiều instance (horizontal scaling), cần S3/MinIO. Kế hoạch sẽ cài đặt `django-storages` với `DEFAULT_FILE_STORAGE` switchable qua env. Bạn xác nhận không?

> [!NOTE]
> **Custom User Model**: Sẽ tạo `CustomUser(AbstractUser)` ngay từ migration đầu tiên (không thể thay đổi sau khi có data). Đây là best practice — bạn đồng ý không?

---

## 🔍 Verification Plan

### Automated Tests
```bash
# Sau khi implement:
poetry run pytest tests/ -v --cov=src --cov-report=html
poetry run ruff check src/
poetry run black --check src/
poetry run bandit -r src/ -ll

# Docker stack
docker-compose up --build -d
curl http://localhost/api/health/  # Expected: {"status": "ok"}
curl http://localhost/api/docs/    # Swagger UI
```

### Manual Verification
- [ ] `docker-compose up` khởi động tất cả 6 services không lỗi
- [ ] `GET /api/health/` trả về `{"db": "ok", "redis": "ok"}`
- [ ] `GET /api/docs/` hiển thị Swagger UI đầy đủ
- [ ] `POST /api/v1/auth/register/` tạo user thành công
- [ ] Flower dashboard tại `localhost:5555` hiển thị Celery workers
- [ ] Lỗi 404 trả về JSON format chuẩn (không phải Django HTML template)

---

## 🗺️ Thứ tự Implementation

```
Phase 1: Foundation
├── pyproject.toml (Poetry setup)
├── src/core/ (base classes, exceptions)
├── src/config/settings/ (4 files)
└── manage.py + .env.example

Phase 2: First Domain (users)
├── domain/ (Entity, VO, Repository interface)
├── application/ (DTOs, Use Cases, UoW)
├── infrastructure/ (Django Model, Repository impl, Migrations)
└── presentation/ (ViewSet, Serializers, URLs v1)

Phase 3: Infrastructure
├── Dockerfile (multi-stage)
├── docker-compose.yml (6 services)
└── docker/nginx/

Phase 4: Quality & Observability
├── .github/workflows/ci.yml
├── Sentry integration
├── Prometheus + django-prometheus
└── Structured logging

Phase 5: Senior Features
├── Soft delete mixin
├── Health check endpoint
├── Rate limiting config
└── Swagger/Redoc setup
```
