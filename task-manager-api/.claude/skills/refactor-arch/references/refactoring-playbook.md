# Refactoring Playbook: Concrete Transformation Patterns

> Practical guide to converting anti-patterns into sustainable solutions.
> Each pattern includes: problem, strategy, and **before/after** code examples.

---

## How to Use This Playbook

1. Identify the dominant anti-pattern.
2. Choose the corresponding transformation pattern.
3. Refactor incrementally.
4. Protect changes with tests.
5. Measure impact (performance, security, maintainability).

---

# 1. God Class → Extract Responsibilities

## Before
```python
class AppManager:
    def save_user(self, user): pass
    def send_email(self, msg): pass
    def generate_report(self): pass
    def process_payment(self): pass
```

## After
```python
class UserService:
    def save_user(self, user): pass

class EmailService:
    def send_email(self, msg): pass

class ReportService:
    def generate_report(self): pass

class PaymentService:
    def process_payment(self): pass
```

## Transformation
- Split responsibilities by domain.
- Apply SRP (Single Responsibility Principle).

---

# 2. SQL Injection → Parameterized Queries

## Before
```python
query = "SELECT * FROM users WHERE email='" + email + "'"
cursor.execute(query)
```

## After
```python
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```

## Transformation
- Replace string concatenation with parameters.
- Prefer secure ORM usage.

---

# 3. Hardcoded Secrets → External Configuration

## Before
```js
const apiKey = "prod_secret_key";
```

## After
```js
const apiKey = process.env.API_KEY;
```

## Transformation
- Use environment variables.
- Use a Secret Manager.

---

# 4. Plain Text Password → Secure Hashing

## Before
```python
user.password = "123456"
```

## After
```python
import bcrypt
user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

## Transformation
- Use bcrypt / Argon2.
- Never store raw passwords.

---

# 5. Broken Authentication → Authorization Middleware

## Before
```js
app.get('/admin/users', (req,res)=> {
  res.send(users)
})
```

## After
```js
app.get('/admin/users', auth, requireRole('admin'), (req,res)=> {
  res.send(users)
})
```

## Transformation
- Enforce authentication.
- Apply RBAC.

---

# 6. Callback Hell → Async/Await

## Before
```js
loadUser(id, function(user){
  loadOrders(user.id, function(orders){
    loadInvoice(orders[0].id, function(inv){
      console.log(inv)
    })
  })
})
```

## After
```js
async function run(){
  const user = await loadUser(id)
  const orders = await loadOrders(user.id)
  const inv = await loadInvoice(orders[0].id)
  console.log(inv)
}
```

## Transformation
- Replace nested callbacks with Promises.
- Create readable linear flow.

---

# 7. N+1 Query Problem → Eager Loading / JOIN

## Before
```python
users = User.all()
for u in users:
    print(u.orders.count())
```

## After
```python
users = User.objects.prefetch_related('orders')
for u in users:
    print(len(u.orders.all()))
```

## Transformation
- Fetch related data in batches.
- Reduce database round-trips.

---

# 8. Duplicate Code → Shared Function

## Before
```python
if not email or '@' not in email:
    raise ValueError()
```
(repeated in multiple files)

## After
```python
def validate_email(email):
    if not email or '@' not in email:
        raise ValueError()
```

## Transformation
- Centralize business rules.
- Improve consistency.

---

# 9. Print Logging → Structured Logging

## Before
```python
print('user created')
```

## After
```python
import logging
logger = logging.getLogger(__name__)
logger.info('user created', extra={'user_id': 10})
```

## Transformation
- Searchable logs.
- Severity levels.

---

# 10. Magic Numbers → Named Constants

## Before
```js
if(timeout > 200){ retry() }
```

## After
```js
const REQUEST_TIMEOUT_MS = 200;
if(timeout > REQUEST_TIMEOUT_MS){ retry() }
```

## Transformation
- Add context to values.
- Easier maintenance.

---

# 11. Tight Coupling → Dependency Injection

## Before
```python
class OrderService:
    def __init__(self):
        self.repo = MySQLOrderRepo()
```

## After
```python
class OrderService:
    def __init__(self, repo):
        self.repo = repo
```

## Transformation
- Easier swapping implementations.
- Better testability.

---

# 12. Fat Controller → Service Layer

## Before
```js
app.post('/checkout', (req,res)=>{
  validate(req.body)
  calculateTaxes()
  chargeCard()
  createInvoice()
})
```

## After
```js
app.post('/checkout', (req,res)=>{
  checkoutService.execute(req.body)
})
```

## Transformation
- Controller orchestrates.
- Business logic belongs in services.

---

# 13. Orphan Data → Cascade / Soft Delete

## Before
```python
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    # orders, invoices, and logs referencing this user are now orphaned
```

## After
```python
def delete_user(user_id):
    cursor.execute("DELETE FROM orders WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM invoices WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

# Or use Foreign Keys with ON DELETE CASCADE:
# CREATE TABLE orders (
#   user_id INT REFERENCES users(id) ON DELETE CASCADE
# );
```

## Transformation
- Define Foreign Keys with ON DELETE CASCADE.
- Alternatively, use soft delete (e.g., `deleted_at` timestamp).
- Ensure referential integrity at the database level.

---

# 14. Global Mutable State → Isolated Context / Dependency Injection

## Before
```python
db_connection = None
current_user = {}

def init():
    global db_connection, current_user
    db_connection = connect_db()
    current_user = {"role": "admin"}

def get_orders():
    global db_connection
    return db_connection.execute("SELECT * FROM orders")
```

## After
```python
class AppContext:
    def __init__(self, db_connection, current_user):
        self.db = db_connection
        self.current_user = current_user

def get_orders(ctx: AppContext):
    return ctx.db.execute("SELECT * FROM orders")

# Usage
ctx = AppContext(db_connection=connect_db(), current_user={"role": "admin"})
orders = get_orders(ctx)
```

## Transformation
- Replace global variables with injected context objects.
- Favor immutability where possible.
- Use dependency injection to pass shared state.

---

# 15. Deprecated/Obsolete APIs → Modern Equivalents

## Before
```python
import cgi  # deprecated since Python 3.11
data = cgi.parse_qs(query_string)

os.popen("ls -la")  # deprecated, insecure

from distutils.core import setup  # deprecated
```
```js
const buf = new Buffer(data)  // deprecated, unsafe
fs.exists(path, callback)     // deprecated
```

## After
```python
from urllib.parse import parse_qs
data = parse_qs(query_string)

import subprocess
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)

from setuptools import setup  # modern replacement
```
```js
const buf = Buffer.from(data)         // safe, explicit
fs.access(path, fs.constants.F_OK, callback)  // modern
```

## Transformation
- Replace deprecated APIs with their modern equivalents.
- Consult official migration guides and changelogs.
- Enable deprecation warnings in linters (`pylint`, `eslint-plugin-deprecation`).

---

# Recommended Prioritization

## Critical
1. SQL Injection
2. Hardcoded Secrets
3. Plain Text Password
4. Broken Authentication

## High Impact
5. God Class
6. Tight Coupling
7. Fat Controller
8. N+1 Query Problem

## Continuous Improvement
9. Duplicate Code
10. Logging
11. Magic Numbers
12. Callback Hell
13. Orphan Data
14. Global Mutable State
15. Deprecated/Obsolete APIs

---

# Refactoring Checklist

- [ ] Is current behavior covered by tests?
- [ ] Did coupling decrease?
- [ ] Did security improve?
- [ ] Did performance improve?
- [ ] Is code easier to read?
- [ ] Can deployment be incremental?

