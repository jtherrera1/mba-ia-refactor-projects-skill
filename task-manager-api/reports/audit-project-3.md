================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask 3.0.0 + Flask-SQLAlchemy 3.1.1
Files:   10 analyzed | ~1060 lines of code

Summary
CRITICAL: 3 | HIGH: 2 | MEDIUM: 4 | LOW: 2

Findings

[CRITICAL] Hardcoded Secrets
File: app.py:13, services/notification_service.py:9-10
Description: SECRET_KEY is hardcoded as 'super-secret-key-123' in app.py.
             SMTP credentials (email_user='taskmanager@gmail.com' and
             email_password='senha123') are hardcoded directly in
             NotificationService.__init__().
Impact: Any git commit exposes credentials. Compromises the application
        secret used for session signing and production email account.
Recommendation: Move all secrets to environment variables loaded via
                python-dotenv. Never commit credentials to source control.

[CRITICAL] Weak Password Hashing
File: models/user.py:29,32
Description: Passwords are hashed with MD5 (hashlib.md5). MD5 is a fast
             cryptographic hash, not a password-hashing function. It has
             no salt, is trivially brute-forced, and is completely broken
             for password storage.
Impact: A database leak exposes all user passwords in seconds via
        rainbow tables or GPU brute-force.
Recommendation: Replace with bcrypt or Argon2 (e.g., flask-bcrypt).
                These are slow by design and salt each hash automatically.

[CRITICAL] Broken Authentication
File: routes/user_routes.py:185-211, routes/task_routes.py:9-300,
      routes/user_routes.py:9-212, routes/report_routes.py:9-224
Description: The /login endpoint returns a fabricated token
             'fake-jwt-token-' + str(user.id). This token is never
             validated on any subsequent request. All destructive routes
             (DELETE /users/<id>, DELETE /tasks/<id>, POST /users, etc.)
             are fully public with no authentication middleware.
Impact: Any unauthenticated client can delete users, tasks, and
        categories. The fake token provides a false sense of security.
Recommendation: Implement JWT (flask-jwt-extended) or session-based auth.
                Protect mutation endpoints with an auth middleware.

[HIGH] Fat Controller / Business Logic in Routes
File: routes/task_routes.py:11-300, routes/user_routes.py:10-212,
      routes/report_routes.py:12-224
Description: Route handlers contain input validation, domain rules
             (overdue calculation, cascade delete, report aggregations),
             and direct ORM calls. Each handler does 4-6 responsibilities
             that should be separated into a controller and service layer.
Impact: Impossible to unit-test business logic in isolation. Any rule
        change requires touching HTTP-layer code. Grows without bound.
Recommendation: Extract business logic into controllers/ and services/.
                Routes should only parse input, call the controller, and
                return the response.

[HIGH] Tight Coupling — Routes Import Directly from Models and DB
File: routes/task_routes.py:1-7, routes/user_routes.py:1-6,
      routes/report_routes.py:1-8
Description: Every route module imports db, Task, User, Category directly.
             There is no abstraction between the HTTP layer and the data
             layer. Changing the ORM or database requires rewriting routes.
Impact: Zero testability without a live database. Violates Dependency
        Inversion Principle. Swapping persistence requires touching every
        route file.
Recommendation: Introduce a controller layer that the routes call. The
                controller handles ORM access, keeping routes decoupled.

[MEDIUM] N+1 Query Problem
File: routes/task_routes.py:41-57, routes/report_routes.py:55-67
Description: get_tasks() loops over all tasks and issues a separate
             User.query.get() and Category.query.get() per task (lines
             41-57). summary_report() issues Task.query.filter_by() for
             each user in a loop (lines 55-67).
Impact: For N tasks, 2N+1 database queries are executed. Severe
        performance degradation at scale.
Recommendation: Use SQLAlchemy eager loading (joinedload / subqueryload)
                to fetch related records in a single query.

[MEDIUM] Duplicate Code — Overdue Logic Repeated 4 Times
File: routes/task_routes.py:30-39, routes/task_routes.py:71-80,
      routes/user_routes.py:170-181, routes/report_routes.py:33-43
Description: The overdue check (compare due_date to utcnow, skip done/
             cancelled statuses) is copy-pasted in four separate places.
             Title validation (len 3-200) is also duplicated between
             create_task and update_task.
Impact: A rule change must be applied in multiple locations. Inconsistent
        fixes are inevitable over time.
Recommendation: Centralise in Task.is_overdue() method (already exists
                but is not used by routes). Extract title validation to a
                shared helper.

[MEDIUM] Deprecated/Obsolete APIs
File: models/task.py:15-16, models/user.py:14, models/category.py:8,
      routes/task_routes.py:67, routes/user_routes.py:29, seed.py:66-67
Description: datetime.utcnow() is deprecated since Python 3.12 (should
             use datetime.now(timezone.utc)). SQLAlchemy 2.0 deprecated
             the legacy Query API: Model.query.get(id) should be replaced
             with db.session.get(Model, id).
Impact: DeprecationWarning noise in logs today; removal in a future Python
        or SQLAlchemy version will break the application silently.
Recommendation: Replace datetime.utcnow() with datetime.now(timezone.utc).
                Replace all .query.get() calls with db.session.get().

[LOW] Print Logging — No Structured Logging
File: routes/task_routes.py:149,153,219,234,
      routes/user_routes.py:83,89,146,
      services/notification_service.py:21,24
Description: print() is used for operational logging throughout the
             codebase. print() is not configurable, has no severity
             levels, and cannot be routed to log aggregators.
Impact: No log severity filtering. Production logs mixed with debug
        output. Impossible to integrate with observability tooling.
Recommendation: Replace print() with Python's logging module. Configure
                a root logger in the application entry point.

[LOW] Magic Numbers / Hardcoded Constants Scattered Across Files
File: routes/task_routes.py:96,99,110,113,
      routes/user_routes.py:64,71
Description: Values like minimum title length (3), maximum title length
             (200), valid priority range (1-5), minimum password length
             (4), and valid role list are repeated inline across multiple
             route files instead of being referenced from a single
             constants module.
Impact: A business rule change (e.g., minimum title length) requires
        finding and updating all occurrences manually.
Recommendation: Consolidate all constants in src/config/settings.py and
                import them wherever needed.

================================
Total: 11 findings
================================
