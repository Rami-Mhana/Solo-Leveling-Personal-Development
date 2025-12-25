Alembic Migrations - Quick Guide

This project includes an Alembic scaffold under `migrations/` to manage schema changes.

Setup (dev)
1. Install alembic in your virtualenv:

   pip install alembic

2. The migrations env is configured to use the Flask app's `SQLALCHEMY_DATABASE_URI` from `create_app()`.
   By default, this will use the application config (see `app/__init__.py`).

3. To run migrations:

   # upgrade to latest
   alembic upgrade head

   # or generate a new migration (edit env.py to include autogenerate target metadata)
   alembic revision --autogenerate -m "describe change"

Notes and recommendations
- Review generated migration scripts before applying to production.
- For production, back up your DB before applying migrations.
- If you prefer to set the DB URL via env var, set `SQLALCHEMY_DATABASE_URI` in your environment before running Alembic.

Example env var (PowerShell):

$env:SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@localhost/dbname"
alembic upgrade head

If you need help creating non-destructive data migrations (e.g., migrating JSON fields into new columns), I can prepare a bespoke migration script.
