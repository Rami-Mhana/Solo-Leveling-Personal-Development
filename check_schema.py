#!/usr/bin/env python
"""Check database schema"""
from app import create_app, db

app = create_app()
app.app_context().push()

from sqlalchemy import inspect

inspector = inspect(db.engine)
columns = inspector.get_columns('user')
print("User table columns:")
print("-" * 50)
for col in columns:
    print(f"{col['name']}: {col['type']}")
