================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~900 lines of code

Summary
CRITICAL: 5 | HIGH: 4 | MEDIUM: 3 | LOW: 2

Findings

[CRITICAL] SQL Injection
File: models.py:22, 35-38, 42-46, 50, 62, 86, 100-103, 109, 114, 122-127, 155-162, 190-195, 205-213, 239, 246, 252-254, 270-285
Description: SQL queries built via string concatenation throughout the entire models.py file.
             Examples:
               cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
               cursor.execute("SELECT * FROM usuarios WHERE email = '" + email + "' AND senha = '" + senha + "'")
               Dynamic search query in buscar_produtos built with raw string concatenation.
Impact: Allows attackers to manipulate queries, exfiltrate data, drop tables, or gain full system access.
Recommendation: Replace all string-concatenated queries with parameterized queries (?, ?) throughout models.py.

[CRITICAL] Hardcoded Secrets
File: app.py:6, controllers.py:270
Description: SECRET_KEY hardcoded directly in source code as "minha-chave-super-secreta-123".
             Additionally, the /health endpoint returns the secret key in the HTTP response body.
Impact: Any developer with repository access (or any user calling /health) obtains the secret key,
        enabling session forgery and token manipulation.
Recommendation: Load SECRET_KEY from environment variable (os.environ). Remove secret_key from health response.

[CRITICAL] Plain Text Password
File: database.py:51-55, models.py:109-114, models.py:60-66
Description: User passwords are stored and queried in plain text. Seed data in database.py inserts
             passwords like "admin123", "123456", "senha123" directly. Login compares plain text passwords.
             get_todos_usuarios returns the senha field to callers.
Impact: A single database breach exposes all user passwords. Violates LGPD/GDPR compliance requirements.
Recommendation: Hash passwords with bcrypt or argon2 on creation. Use constant-time comparison on login.
                Never return senha in API responses.

[CRITICAL] Broken Authentication
File: app.py:43-63
Description: Two unprotected administrative endpoints exist with no authentication:
               /admin/reset-db (POST) — deletes all data from all tables
               /admin/query (POST)   — executes arbitrary SQL from request body
             These endpoints are exposed to any HTTP client with no auth checks whatsoever.
Impact: Any unauthenticated user can wipe the entire database or execute arbitrary SQL,
        leading to full data loss or system compromise.
Recommendation: Remove /admin/query entirely (or restrict to local-only). Protect /admin/* routes
                with authentication middleware and admin role enforcement.

[CRITICAL] God Class / Flat Architecture (No Layer Separation)
File: models.py:1-315
Description: models.py acts as a God module — it contains data access queries, business logic,
             discount calculation rules, stock management, and order orchestration all in one file.
             criar_pedido handles stock validation, total calculation, and inventory deduction.
             relatorio_vendas contains complex discount tier business logic.
             controllers.py also directly imports get_db and executes SQL (health_check).
Impact: Impossible to test business logic in isolation. Any change risks unintended side-effects.
        Completely violates MVC separation of concerns and Single Responsibility Principle.
Recommendation: Extract business logic to a service layer. Keep models as pure data-access repositories.
                Move discount and order logic to dedicated service classes.

[HIGH] Sensitive Data Exposure via API Response
File: controllers.py:263-278
Description: The /health endpoint returns sensitive configuration details in the response body:
               "secret_key": "minha-chave-super-secreta-123"
               "debug": True
               "db_path": "loja.db"
             Also, listar_usuarios returns the senha field for all users (models.py:78).
Impact: Attackers can harvest credentials and internal config details from a public endpoint.
        User passwords exposed in list endpoint violate data minimization principles.
Recommendation: Strip all sensitive fields from API responses. Health check should only report
                operational status (db connected: yes/no), never config values.

[HIGH] Fat Controller
File: controllers.py:62-100, controllers.py:195-220, controllers.py:222-237
Description: criar_produto performs extensive inline validation (field presence, length, value range,
             category enum). criar_pedido fires notification side-effects (email, SMS, push) inline.
             atualizar_status_pedido fires conditional notifications inline.
             These are business-layer concerns embedded in HTTP handler functions.
Impact: Controllers are untestable without HTTP context. Business rules cannot be reused.
        Notification logic is hardcoded and cannot be swapped or extended.
Recommendation: Extract validation to a dedicated validator or schema layer. Move notification
                logic to a NotificationService called from controllers.

[HIGH] Global Mutable State
File: database.py:4-5, database.py:9
Description: A module-level global variable db_connection = None is mutated by get_db().
             The connection is created with check_same_thread=False to suppress a threading warning,
             hiding the underlying concurrency risk rather than fixing it.
Impact: Under concurrent requests, multiple threads share a single connection with no locking,
        leading to potential data corruption or race conditions.
Recommendation: Use Flask's g context object (flask.g) for per-request DB connections,
                or use a connection pool with proper thread isolation.

[HIGH] Tight Coupling
File: app.py:3-4, controllers.py:3, controllers.py:261
Description: app.py imports controllers directly (import controllers). controllers.py imports models
             directly (import models) and also imports get_db directly for the health_check function,
             bypassing the model layer entirely. All modules are hardwired to each other with no
             abstraction boundary.
Impact: Replacing any component (e.g., switching from SQLite to PostgreSQL) requires changes
        across all layers. Unit testing individual components is not possible without loading all layers.
Recommendation: Define interfaces or repository abstractions. Inject dependencies rather than
                importing concrete implementations directly.

[MEDIUM] N+1 Query Problem
File: models.py:157-192, models.py:197-230
Description: get_pedidos_usuario and get_todos_pedidos both execute nested queries:
             for each pedido -> query itens_pedido, for each item -> query produtos.
             A list of 10 orders with 5 items each triggers 10 + 50 + 50 = 110 queries.
Impact: Severe performance degradation as order count grows. Database becomes a bottleneck.
Recommendation: Replace with JOIN queries that fetch pedidos + itens + produto names in one
                or two queries. Example:
                SELECT p.*, ip.*, prod.nome FROM pedidos p
                JOIN itens_pedido ip ON ip.pedido_id = p.id
                JOIN produtos prod ON prod.id = ip.produto_id
                WHERE p.usuario_id = ?

[MEDIUM] Duplicate Code
File: models.py:12-21, models.py:28-37 (get_produto_por_id), models.py:284-293 (buscar_produtos)
     models.py:157-192 vs models.py:197-230
Description: The product serialization dictionary (id, nome, descricao, preco, estoque, categoria,
             ativo, criado_em) is duplicated verbatim in three separate functions.
             get_pedidos_usuario and get_todos_pedidos are structurally identical — the only difference
             is whether a WHERE clause filters by usuario_id.
Impact: Any change to the product schema requires updates in three separate locations,
        increasing the risk of inconsistency.
Recommendation: Extract a serialize_produto(row) helper function. Merge the two pedido-listing
                functions with an optional usuario_id parameter.

[MEDIUM] Orphan Data
File: database.py:24-49
Description: No FOREIGN KEY constraints are defined in any table DDL. Deleting a produto does not
             cascade to itens_pedido. Deleting a usuario does not cascade to pedidos.
             The /admin/reset-db endpoint also deletes in the correct order by hand rather than
             relying on referential integrity.
Impact: Deleting a product or user leaves dangling references in related tables, causing data
        integrity errors and potential NullPointerException-equivalent bugs at runtime.
Recommendation: Add FOREIGN KEY constraints with ON DELETE CASCADE (or ON DELETE RESTRICT).
                Enable foreign key enforcement in SQLite with PRAGMA foreign_keys = ON.

[LOW] Print Logging
File: controllers.py:7, 48, 82, 145, 172, 183, 198, 200, 217, 227
Description: print() is used throughout controllers.py for logging (e.g., "Listando X produtos",
             "Produto criado com ID: X", "ENVIANDO EMAIL: ...", "NOTIFICAÇÃO: ...").
Impact: Logs are unstructured, cannot be filtered by severity level, and will appear as raw stdout
        in production. No log rotation, correlation IDs, or structured format.
Recommendation: Replace all print() calls with Python's logging module using appropriate levels
                (logger.info, logger.warning, logger.error).

[LOW] Magic Numbers
File: models.py:245-252 (relatorio_vendas), controllers.py:76-79 (criar_produto)
Description: Discount tier thresholds (10000, 5000, 1000) and rates (0.1, 0.05, 0.02) are
             hardcoded inline in relatorio_vendas with no named constants.
             Product name length limits (2, 200) are hardcoded in criar_produto validation.
Impact: Values lack context. Changing a discount threshold requires finding and editing raw numbers
        scattered across the code, with no documentation of their business meaning.
Recommendation: Define named constants (e.g., DISCOUNT_TIER_HIGH = 10000, NOME_MIN_LEN = 2)
                in a config or constants module.

================================
Total: 14 findings
================================
