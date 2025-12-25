"""Create and seed the database for local development.

Usage:
    python create_db.py

This will create the SQLite DB defined by the app factory and insert a demo
user. Run this once after setting up the virtualenv.
"""
from app import create_app
from app.models import db, User


def seed(app):
    with app.app_context():
        # Drop and recreate tables to ensure schema matches models during development
        db.drop_all()
        db.create_all()

        if not User.query.filter_by(username='testuser').first():
            u = User(username='testuser', email='testuser@example.com')
            u.set_password('password')
            db.session.add(u)
            db.session.commit()
            print('Created demo user testuser with password "password"')
        else:
            print('Demo user already exists')


if __name__ == '__main__':
    app = create_app()
    seed(app)
    

