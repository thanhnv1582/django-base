---
name: django-ddd-clean-arch
description: Comprehensive Full-Stack Standard. Enforces 4-layer DDD (API) + Nexus Digital Atelier (Dashboard MVC). Includes coding patterns, directory structures, and layout consistency rules.
---

# Django DDD & Dashboard Full-Stack Master Standard

This skill defines the definitive architectural and design standards for this project. It combines **Domain-Driven Design (DDD)** for the core logic and **Nexus Digital Atelier** for the management UI.

## I. Architectural Layers (DDD Core)

Every module MUST be strictly divided into four layers to ensure separation of concerns.

### 1. Domain Layer (`domain/`)
- **Pure Python**: Zero dependencies on Django or third-party frameworks.
- **Entities**: Business objects with identity (inherit from `BaseEntity`).
- **Value Objects**: Immutable objects defined by attributes (e.g., `Email`, `Price`).
- **Repositories (Interfaces)**: Use `Protocol` or `ABC` to define data contracts.
- **Events**: Domain events (e.g., `ProductCreated`) to decouple side effects.

### 2. Application Layer (`application/`)
- **Use Cases**: Orchestrate domain entities to perform a single business action.
- **Services**: Complex logic involving multiple entities or external systems.
- **DTOs**: Data Transfer Objects for input/output sanitization.

### 3. Infrastructure Layer (`infrastructure/`)
- **Models**: Django ORM models.
- **Mapping**: Infrastructure models MUST implement `to_domain()` to map to Domain Entities.
- **Repositories**: Concrete Django ORM implementations of Domain interfaces.

### 4. Presentation Layer (`presentation/`)
- **REST API (v1/api/)**: ViewSets and Serializers.
- **API Documentation**: MANDATORY use of `@extend_schema` for Swagger/drf-spectacular.

---

## II. Dashboard MVC Layer (Nexus Design)

Every entity must have a management UI in the `dashboard` app following the **Nexus Digital Atelier** style.

### 1. Visual Standards (Light Mode)
- **Typography**: `Manrope` for Headlines, `Inter` for Body/Data.
- **No-Border Rule**: Borders are strictly forbidden. Use background depth (`surface` vs `bg-page`) and ambient shadows (`rgba(25, 28, 30, 0.06)`).
- **Primary Color**: Nexus Indigo (`#4F46E5`).

### 2. Implementation
- **Layout**: MUST extend `base_dashboard.html`.
- **Interactivity**: Use **HTMX** for high-productivity actions (status toggles, deletions) to provide a SPA-like experience.

---

## III. Full-Stack Generation Workflow

When creating a new entity `X`:
1.  **Dual-Track Development**: Build the DDD Backend and the Nexus Dashboard simultaneously.
2.  **Automatic CRUD**: Generate Create, List, Detail, Update, Toggle, and Delete endpoints & views.

---

## IV. Reference Directory Structure

```
src/apps/products/
├── domain/
│   ├── entities/            # ProductEntity
│   ├── value_objects/       # Price, Quantity
│   ├── repositories/        # IProductRepository (Interface)
│   └── events/              # ProductCreated
├── application/
│   ├── use_cases/           # CreateProductUseCase, ListProductsUseCase
│   ├── dtos/                # ProductDTOs
│   └── services/            # ProductService
├── infrastructure/
│   ├── models/              # ProductModel (with to_domain())
│   └── repositories/        # DjangoProductRepository
└── presentation/
    ├── v1/api/              # DRF ViewSets/Serializers (with @extend_schema)
    └── v1/urls.py
```

---

## V. Vital Code Patterns

### 1. Domain Entity & Value Object
```python
@dataclass
class ProductEntity(BaseEntity):
    name: str
    price: Price
    def apply_discount(self, percent: Decimal):
        self.price = self.price.discount(percent)
```

### 2. Infrastructure Mapping
```python
class ProductModel(UUIDModel):
    name = models.CharField(...)
    price = models.DecimalField(...)
    
    def to_domain(self) -> ProductEntity:
        return ProductEntity(id=self.id, name=self.name, price=Price(self.price))
```

### 3. Dashboard HTMX Toggle
```html
<div class="switch {% if active %}active{% endif %}" 
     hx-post="{% url 'toggle' %}" 
     hx-swap="outerHTML">
    <div class="handle"></div>
</div>
```

---

## VI. Implementation Checklist
- [ ] NO Django imports in `domain/`.
- [ ] `to_domain()` maps ALL infrastructure fields to domain fields.
- [ ] Swagger tags and responses are defined via `@extend_schema`.
- [ ] Sidebar link added to `base_dashboard.html`.
- [ ] No `1px solid` border in CSS; use `shadow-ambient` and `surface` shifts.
