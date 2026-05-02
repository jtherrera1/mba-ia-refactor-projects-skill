# Architecture Guidelines

## Objective
Define the **target MVC pattern** for automatically analyzed projects, clearly separating responsibilities between **Models**, **Views/Routes**, and **Controllers**.

Also establishes the differences between the **desired architecture** and the findings of the **Project Analysis Heuristics**.

---

# 1. Target MVC Pattern

## 1.1 Models (Data and Domain Layer)
**Responsibilities:**
- Represent business entities.
- Domain validation rules.
- ORM mapping / database access.
- Relationships between entities.
- Queries encapsulated in repositories when applicable.

**Should contain:**
- `User`, `Order`, `Invoice`, etc.
- Persistent Schemas / Entities / DTOs.
- Model-related migrations.

**Should NOT contain:**
- HTTP code.
- View rendering.
- Routing rules.
- UI logic.

---

## 1.2 Views / Routes (Input and Presentation Layer)
**Responsibilities:**
- Define endpoints and URLs.
- Map requests to controllers.
- Render templates/views when server-side frontend exists.
- Basic response serialization.

**Should contain:**
- `routes/web.php`
- `routes/api.php`
- `urls.py`
- `express.Router()`
- templates (`.html`, `.twig`, `.blade.php`, etc.)

**Should NOT contain:**
- SQL queries.
- Complex business rules.
- Direct database access.

---

## 1.3 Controllers (Orchestration)
**Responsibilities:**
- Receive request.
- Validate input.
- Call services/models.
- Orchestrate flow.
- Return response.

**Should contain:**
- CRUD handlers.
- HTTP use cases.
- Error handling.

**Should NOT contain:**
- Inline SQL.
- Extensive HTML.
- Complex domain rules persisted in the controller.

---

# 2. Recommended Structure

```text
src/
 ├── models/
 ├── controllers/
 ├── routes/
 ├── views/
 ├── services/
 ├── repositories/
 └── config/
```

> `services/` and `repositories/` are acceptable MVC extensions for better maintainability.

---

# 3. Difference Between Target MVC vs Project Analysis

## What is Project Analysis
It is the automatic discovery step based on heuristics to identify:
- language
- framework
- database
- current architecture
- entrypoints
- structural risks

## What is different from the Guidelines
**Project Analysis** describes **how the project looks today**.
**Architecture Guidelines** describe **how the project should look**.

---

# 4. Project Analysis Items that DO NOT Match the Target MVC

## 4.1 Layered Architecture
Structure:
```text
controller/
service/
repository/
dto/
```
**Difference:** adds extra layers beyond classic MVC.

## 4.2 Clean Architecture
Structure:
```text
domain/
application/
infrastructure/
interfaces/
```
**Difference:** separation by dependency and use cases, not by MVC.

## 4.3 Hexagonal Architecture
Structure:
```text
ports/
adapters/
core/
```
**Difference:** focus on domain isolation and external integration.

## 4.4 Microservices
**Difference:** multiple independent services; MVC may exist within each service, but does not define a distributed system.

## 4.5 Script Chaos / Legacy Flat Structure
Indicators:
- SQL mixed with routes
- logic at root level
- absence of layers

**Difference:** completely violates MVC separation.

---

# 5. Compliance Rules

## MVC-Compliant
- `models/` exists
- `controllers/` exists
- `routes/` or `views/` exists
- Controllers without inline SQL
- Models without HTTP code
- Routes only map handlers

## Non-Compliant
- Controller accesses database directly
- View contains business logic
- Model responds to HTTP request
- Large files with multiple responsibilities

---

# 6. Automatic Rules for Auditing

## Suggested Score
- Correct folder structure: +30
- Separation of responsibilities: +30
- Thin controllers: +20
- Organized models: +10
- Clean routes: +10

## Penalties
- SQL in controller: -20
- Business logic in route: -20
- Flat architecture: -30
- Circular coupling: -20
