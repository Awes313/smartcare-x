# SmartCare X

**Intelligent Healthcare Management Platform** — a backend-heavy Flask hospital SaaS covering patient booking, doctor workflows, front-desk operations, and admin analytics.

## Tech Stack

- **Backend:** Python 3, Flask (application factory + Blueprints), Flask-Login, Flask-Mail, Flask-WTF, Flask-Migrate, SQLAlchemy ORM
- **Database:** SQLite (dev) → PostgreSQL (prod)
- **Frontend:** Jinja2, Bootstrap 5, Bootstrap Icons, Chart.js, minimal vanilla JS
- **PDF/CSV:** ReportLab, built-in `csv`
- **Deployment:** Render (Gunicorn)

## Roles

Patient · Doctor · Receptionist · Admin — each with its own Blueprint, dashboard, and permissions.

## Local Setup

```bash
git clone <your-repo-url>
cd smartcare-x

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # then edit SECRET_KEY, MAIL_* settings, etc.

flask db init
flask db migrate -m "Initial schema"
flask db upgrade

flask seed-db                   # creates admin account + starter departments/medicines

flask run
```

Default seeded admin login: `admin@smartcarex.local` / `ChangeMe123!` (override via `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD` env vars before seeding). **Change this password immediately in any non-local environment.**

## Project Structure

```
smartcare-x/
├── app.py                  # Entry point
├── config.py                # Dev / Prod / Testing config classes
├── requirements.txt
├── Procfile
├── .env.example
└── smartcare/
    ├── __init__.py          # create_app() factory
    ├── extensions.py        # db, login_manager, mail, csrf, migrate
    ├── models/               # SQLAlchemy models (one file per domain)
    ├── auth/ patient/ doctor/ reception/ admin/ main/   # Blueprints
    ├── services/             # Business logic (appointments, billing, inventory, reports...)
    ├── utils/                 # Decorators, pagination, PDF/CSV export, file uploads, validators
    ├── emails/                # Mailer + email templates
    ├── static/                # CSS, JS, uploaded files
    └── templates/             # Jinja2 templates, organized per blueprint
```

## Key Design Decisions

- **Business logic lives in `services/`, not in routes or templates.** Routes stay thin: parse input, call a service, render a template.
- **Role-based access** is enforced via `@role_required(...)` decorators and a per-blueprint `before_request` guard, not scattered `if` checks.
- **PDFs** (prescriptions, receipts, reports) are generated with ReportLab — pure Python, no system dependencies, so it deploys cleanly on Render's free tier.
- **Stock deduction** happens atomically with prescription creation (`prescription_service.py`), so a prescription is never saved without reserving its medicine stock.

## Deploying to Render

1. Push this repo to GitHub.
2. Create a new **Web Service** on Render, pointing at the repo.
3. Add a **PostgreSQL** instance and copy its connection string into the `DATABASE_URL` environment variable.
4. Set the remaining environment variables from `.env.example` (`SECRET_KEY`, `MAIL_*`, etc.) in the Render dashboard.
5. Render will run `pip install -r requirements.txt`, then the `Procfile`'s `release` step (`flask db upgrade`) before starting `web: gunicorn app:app`.
6. Run `flask seed-db` once via Render's shell to create the initial admin account.

## License

Built as a portfolio/demo project. Adapt freely for coursework, interviews, or as a starting point for a real deployment (swap the seeded admin credentials and review the security checklist below first).

## Pre-Production Checklist

- [ ] Set a strong, unique `SECRET_KEY`
- [ ] Change the seeded admin password
- [ ] Configure real SMTP credentials for `MAIL_*`
- [ ] Confirm `SESSION_COOKIE_SECURE=True` in production (already default via `ProductionConfig`)
- [ ] Set an appropriate `DEFAULT_TAX_RATE` in `services/billing_service.py` for your region
