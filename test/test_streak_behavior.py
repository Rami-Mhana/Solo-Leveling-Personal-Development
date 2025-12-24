import sys
import os
from datetime import date, timedelta

# Ensure repo root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, User


def run_tests():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.drop_all()
        db.create_all()

        client = app.test_client()

        # Create a user directly
        u = User(username='streaker', email='streak@example.com')
        u.set_password('pass')
        db.session.add(u)
        db.session.commit()

        # 1) If last_login_date is yesterday, streak increments
        yesterday = date.today() - timedelta(days=1)
        u.last_login_date = yesterday
        u.streak_count = 2
        db.session.add(u)
        db.session.commit()

        resp = client.post('/login', data={'username': 'streaker', 'password': 'pass'}, follow_redirects=True)
        u = User.query.filter_by(username='streaker').first()
        if u.streak_count == 3:
            print('STREAK INCREMENT: PASS')
        else:
            print('STREAK INCREMENT: FAIL', u.streak_count)
            return

        # 2) If last_login_date is before yesterday, streak resets to 1
        three_days_ago = date.today() - timedelta(days=3)
        u.last_login_date = three_days_ago
        u.streak_count = 5
        db.session.add(u)
        db.session.commit()

        resp = client.post('/login', data={'username': 'streaker', 'password': 'pass'}, follow_redirects=True)
        u = User.query.filter_by(username='streaker').first()
        if u.streak_count == 1:
            print('STREAK RESET: PASS')
        else:
            print('STREAK RESET: FAIL', u.streak_count)
            return

        # 3) If last_login_date is today, streak unchanged
        today = date.today()
        u.last_login_date = today
        u.streak_count = 4
        db.session.add(u)
        db.session.commit()

        resp = client.post('/login', data={'username': 'streaker', 'password': 'pass'}, follow_redirects=True)
        u = User.query.filter_by(username='streaker').first()
        if u.streak_count == 4:
            print('STREAK NO-OP: PASS')
        else:
            print('STREAK NO-OP: FAIL', u.streak_count)
            return

        print('ALL STREAK TESTS PASSED')


if __name__ == '__main__':
    run_tests()
