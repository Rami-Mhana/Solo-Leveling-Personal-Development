import sys
import os
# Ensure repo root is on sys.path so 'app' package can be imported when running this script from test/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, User


def run_tests():
    app = create_app()
    # Use an in-memory SQLite database for isolated tests
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        # Ensure a fresh in-memory database for this test run
        db.drop_all()
        db.create_all()
        # Regression for user auth flow
        client = app.test_client()

        username = 'autotestuser'
        email = 'autotest@example.com'
        password = 'testpass123'

        # 1) Register
        resp = client.post('/register', data={
            'username': username,
            'email': email,
            'password': password,
        }, follow_redirects=True)

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            print('REGISTER: PASS')
        else:
            print('REGISTER: FAIL')
            print('Response status:', resp.status_code)
            print(resp.get_data(as_text=True))
            sys.exit(2)

        # 2) Login
        resp = client.post('/login', data={
            'username': username,
            'password': password,
        }, follow_redirects=True)

        if resp.status_code == 200 and username in resp.get_data(as_text=True):
            print('LOGIN: PASS')
        else:
            print('LOGIN: FAIL')
            print('Status:', resp.status_code)
            print(resp.get_data(as_text=True))
            sys.exit(3)

        # 3) View profile
        resp = client.get('/profile')
        if resp.status_code == 200 and username in resp.get_data(as_text=True):
            print('PROFILE VIEW: PASS')
        else:
            print('PROFILE VIEW: FAIL')
            print('Status:', resp.status_code)
            print(resp.get_data(as_text=True))
            sys.exit(4)

        # 4) Edit profile (change username)
        new_username = username + '2'
        resp = client.post('/profile', data={
            'username': new_username,
            'email': email,
            # leave password blank to keep same
            'password': ''
        }, follow_redirects=True)

        updated = User.query.filter_by(username=new_username).first()
        if updated:
            print('PROFILE EDIT: PASS')
        else:
            print('PROFILE EDIT: FAIL')
            print('Response status:', resp.status_code)
            print(resp.get_data(as_text=True))
            sys.exit(5)

        print('ALL TESTS PASSED')


if __name__ == '__main__':
    run_tests()
