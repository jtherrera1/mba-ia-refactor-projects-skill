# Project Analysis Heuristics — Detection Heuristics

## Purpose
Detailed reference guide for automatic project discovery during Skill Phase 1.

This document helps detect:
- Programming language
- Framework
- Build/runtime tools
n- Database technology
- Deployment model
- Current architecture style
- Entry points
- Risk indicators

---

# 1. Language Detection Heuristics

## JavaScript / TypeScript
Indicators:
- package.json
- package-lock.json
- yarn.lock
- pnpm-lock.yaml
- tsconfig.json
- *.js / *.ts files

Confidence:
- package.json + src/*.ts = HIGH
- only js files = MEDIUM

## Python
Indicators:
- requirements.txt
- pyproject.toml
- Pipfile
- setup.py
- *.py files

Confidence:
- requirements + app.py/manage.py = HIGH

## Java
Indicators:
- pom.xml
- build.gradle
- gradlew
- src/main/java

## PHP
Indicators:
- composer.json
- artisan
- *.php

## .NET
Indicators:
- *.csproj
- *.sln
- Program.cs

## Go
Indicators:
- go.mod
- main.go

## Rust
Indicators:
- Cargo.toml
- src/main.rs

---

# 2. Framework Detection Heuristics

## Node.js
### Express
- dependency: express
- app.use(...)
- router = express.Router()

### NestJS
- @Module()
- main.ts
- @Controller()

### Next.js
- next.config.js
- pages/
- app/

## Python
### Flask
- from flask import Flask
- @app.route

### Django
- manage.py
- settings.py
- urls.py

### FastAPI
- from fastapi import FastAPI
- @app.get()

## Java
### Spring Boot
- @SpringBootApplication
- application.properties
- @RestController

## PHP
### Laravel
- artisan
- routes/web.php
- app/Http/Controllers

## .NET
### ASP.NET Core
- Program.cs
- builder.Services
- Controllers/

---

# 3. Database Detection Heuristics

## Relational Databases

### PostgreSQL
Indicators:
- `postgres://`
- `postgresql://`
- psycopg2
- pg package
- SQLAlchemy postgres dialect
- port 5432
- docker image `postgres`

### MySQL / MariaDB
Indicators:
- `mysql://`
- mysql2
- mysqlclient
- pymysql
- port 3306
- docker image `mysql`, `mariadb`

### SQL Server
Indicators:
- mssql package
- `System.Data.SqlClient`
- `Microsoft.Data.SqlClient`
- port 1433

### SQLite
Indicators:
- sqlite3
- `*.db`
- `*.sqlite`
- local file connection strings

### Oracle
Indicators:
- cx_Oracle
- Oracle.ManagedDataAccess
- port 1521

## NoSQL Detection

### MongoDB
Indicators:
- mongoose
- pymongo
- mongodb://
- collections/

### Redis
Indicators:
- redis package
- ioredis
- cache configs
- port 6379

### Elasticsearch / OpenSearch
Indicators:
- elasticsearch package
- search client configs


## Schema File Inspection

Inspect these files/folders:

### SQL Files
- `/db/*.sql`
- `/database/*.sql`
- `/schema/*.sql`
- `/migrations/*.sql`
- `/scripts/*.sql`

### Migration Frameworks
- Alembic
- Flyway
- Liquibase
- Prisma migrations
- Sequelize migrations
- Django migrations
- Laravel migrations
- EF migrations
- Rails migrations

### ORM Models
- models/*.py
- entities/*.ts
- schema.prisma
- models/*.cs
- JPA entities


## Table Detection Rules

Search for:

```sql
CREATE TABLE users (
CREATE TABLE orders (
ALTER TABLE
```

Extract:
- table name
- schema name
- columns
- data types
- defaults
- constraints
- indexes

Example Output:

```txt
Table: users
Schema: public
Columns:
- id UUID PK
- email VARCHAR(255)
- created_at TIMESTAMP
```

---

## Schema Detection Rules

Detect schemas such as:
- public
- auth
- sales
- finance
- hr
- custom schemas

Patterns:

```sql
CREATE SCHEMA finance;
finance.orders
auth.users
```

Output:

```txt
Schemas Found:
- public
- finance
- auth
```

# 4. Architecture Mapping Heuristics

## MVC
Indicators:
- models/
- controllers/
- routes/ or views/
- templates/

## Layered Architecture
Indicators:
- controller/
- service/
- repository/
- dto/

## Clean Architecture
Indicators:
- domain/
- application/
- infrastructure/
- interfaces/

## Hexagonal Architecture
Indicators:
- ports/
- adapters/
- core/

## Microservices
Indicators:
- multiple deployable apps
- docker-compose with many services
- API gateway
- separate databases

## Monolith
Indicators:
- single repo
- single deploy artifact
- many modules coupled

## Script Chaos / Legacy Flat Structure
Indicators:
- large root folder
- mixed routes + SQL + business logic
- no layers


# 5. Entry Point Detection

Search for:
- app.py
- main.py
- server.js
- index.js
- Program.cs
- Main.java
- manage.py
- artisan serve

Also inspect:
- package.json scripts.start
- Docker CMD / ENTRYPOINT
- Procfile


# 6. Deployment Model Detection

## Containers
- Dockerfile
- docker-compose.yml
- kubernetes manifests

## Serverless
- serverless.yml
- lambda handlers
- vercel.json

## Traditional VM
- systemd scripts
- nginx configs
- pm2 ecosystem file

# 7. Deprecated API Detection Heuristics

## Purpose
Identify obsolete, deprecated, or soon-to-be-removed APIs that increase maintenance risk and upgrade cost.

## Generic Indicators
- Compiler warnings mentioning `deprecated`
- Runtime warnings (`DeprecationWarning`)
- Documentation tags: `@deprecated`, `[Obsolete]`
- Release notes mentioning removal
- Static analyzer findings
- Legacy imports no longer recommended

## Confidence Levels
- Explicit language annotation + direct usage = HIGH
- Warning in build logs = HIGH
- Name match against known deprecated symbol list = MEDIUM
- Community recommendation only = LOW

---

## Java
Indicators:
- `@Deprecated`
- `javac -Xlint:deprecation`
- Calls to `Thread.stop()`, `Date.getYear()`
- Deprecated Spring / Jakarta APIs

Detection Sources:
- Source AST
- Build logs
- IDE inspections

---

## C# / .NET
Indicators:
- `[Obsolete]`
- Compiler warning CS0618
- Calls to legacy APIs like `Thread.Suspend()`

Detection Sources:
- Roslyn analyzers
- Build output
- Visual Studio warnings

---

## Python
Indicators:
- `DeprecationWarning`
- Imports like `imp`, `distutils`
- Deprecated framework methods

Detection Sources:
- Runtime tests
- Ruff / pylint / pyupgrade
- Dependency changelogs

---

## JavaScript / TypeScript
Indicators:
- JSDoc `@deprecated`
- TypeScript editor warnings
- Node.js deprecated APIs (`new Buffer()`)
- Deprecated framework lifecycle methods

Detection Sources:
- ESLint
- TypeScript compiler
- Package release notes

---

## PHP
Indicators:
- Deprecated notices in runtime
- `mysql_*` functions
- Framework methods marked deprecated

Detection Sources:
- PHPStan
n- Psalm
- Runtime logs

---

## Go
Indicators:
- Comments containing `Deprecated:`
- Old stdlib replacements noted in docs

Detection Sources:
- `go doc`
- staticcheck

---

## Rust
Indicators:
- `#[deprecated]`
- Cargo warnings

Detection Sources:
- `cargo check`
- clippy

---

## Risk Scoring Rules
- Deprecated but replacement available = Medium
- Removal scheduled next major version = High
- Security-related deprecation = Critical
- Widely used deprecated API across many files = High

---

## Example Output

```txt
Deprecated API Findings:
- Java: Thread.stop() in UserWorker.java:44 (HIGH)
- Python: import imp in loader.py:3 (MEDIUM)
- Node.js: new Buffer() in auth.js:18 (HIGH)
```

---

## Recommended Actions
- Replace with supported API
- Create migration backlog item
- Block new usages in CI
- Add linter/compiler deprecation gates
- Prioritize high-frequency occurrences

