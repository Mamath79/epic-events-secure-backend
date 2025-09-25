# Epic Events CRM — Secure Python + SQL (P12)

> **Educational project (OpenClassrooms)** — design a secure, role‑aware back‑end architecture in **Python + SQL** for a small CRM. Console‑driven UX with a layered codebase.

---

## ✨ Key features

- 🔐 **Authentication**: login with **JWT** session tokens
- 🧂 **Password hashing**: **Argon2**
- 👥 **RBAC**: department‑based permissions (e.g., Sales / Support / Management)
- 🗃️ **Relational data model**: customers, contracts, events & assignments
- 🧱 **Layered architecture**: `controllers` → `services` → `repositories` (SQLAlchemy)
- 🧹 Quality tooling: **flake8**, **black**, **pytest** (with coverage)

> This codebase is intended for learning and portfolio demonstration. Harden further before production.

---

## 🧱 Tech stack

- **Python 3.10+**
- **SQLAlchemy** (ORM)
- **MySQL** (dev/prod) — SQLite possible for local experiments
- **PyJWT** (JWT), **argon2‑cffi** (password hashing)
- Tooling: **flake8**, **black**, **pytest**, **coverage**

---

## 📦 Project structure (excerpt)

```
.
├─ main.py                         # Application entry point (CLI)
├─ config.py                       # Settings (DB URL, secrets, etc.)
├─ requirements.txt
├─ epic_events_databse.png         # Database schema overview
└─ crm/
   ├─ controllers/                 # I/O & command routing
   ├─ services/                    # Business rules (RBAC, validations)
   ├─ repositories/                # DB access via SQLAlchemy
   ├─ models/                      # ORM models (User, Customer, Contract, Event...)
   ├─ security/                    # auth, JWT, password hashing
   └─ utils/                       # helpers (validation, formatting, etc.)
```

> Names may vary slightly; see the code for the exact modules present in this repository.

---

## 🚀 Quickstart

### 1) Clone & create a virtual environment

```bash
git clone https://github.com/Mamath79/OC_P12_D-veloppez-une-architecture-back-end-securisee-avec-Python-et-SQL.git
cd OC_P12_D-veloppez-une-architecture-back-end-securisee-avec-Python-et-SQL
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment

Create a `.env` file (or edit `config.py`) with your database and secret settings:

```ini
# Example .env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/epic_events
JWT_SECRET=change-me
JWT_ACCESS_TTL_MINUTES=60
ARGON2_TIME_COST=2
ARGON2_MEMORY_COST=65536
ARGON2_PARALLELISM=2
```

> You can also use SQLite locally: `sqlite:///./epic_events.db`

### 3) Initialize DB & run

```bash
python main.py
```

- The app will connect to the DB and, if implemented, create tables from SQLAlchemy models.
- Follow the interactive prompts to **sign in**, **create customers**, **contracts**, **events**, and **assign support**.

---

## 👥 Roles & permissions (overview)

- **Sales**: manage customers and contracts; create events tied to signed contracts
- **Management**: review/assign events to support staff; oversee contracts
- **Support**: handle assigned events (status, notes)

Permissions are enforced in the `services` layer and checked in controllers before executing a command.

---

## 🧪 Tests & quality

Run tests (if present):

```bash
pytest -q --maxfail=1
```

Measure coverage:

```bash
pytest -q --cov=crm --cov-report=term-missing
```

Code style / lint:

```bash
black .
flake8 .
```

---

## 🛡️ Security notes

- **Passwords** are hashed with **Argon2** (no plaintext storage)
- **JWT** tokens carry minimal claims and short TTLs; refresh as needed
- **Parameterized queries** via SQLAlchemy protect against SQL injection
- Secrets should be **kept out of VCS**; use environment variables for config

---

## 🗺️ Database schema (high level)



Typical entities:

- `User` (department/role)
- `Customer`
- `Contract` (amount, status, linked to Customer & Sales)
- `Event` (date, location, support assignment, status)

---

## 🛳️ Deployment (example)

- Use **MySQL** or **PostgreSQL** with managed backups
- Export secrets to the environment (`DATABASE_URL`, `JWT_SECRET`)
- Run as a **systemd service** or container; add structured logging
- Monitor with Sentry/ELK; restrict DB network access

---

## 🧭 Roadmap ideas

- Replace CLI with a **REST API** (FastAPI/Django REST Framework)
- Admin interface for management
- Email notifications for contract/event status
- Fine‑grained permissions & audit logging

---

## 👤 Author

**Mathieu Vieillefont**\
LinkedIn: [https://www.linkedin.com/in/mathieu-vieillefont/](https://www.linkedin.com/in/mathieu-vieillefont/)\
Email: [mathieu.vieillefont@gmail.com](mailto\:mathieu.vieillefont@gmail.com)

