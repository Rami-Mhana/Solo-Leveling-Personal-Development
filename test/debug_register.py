import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    # Start with a clean DB for this debug
    db.drop_all()
    db.create_all()

    client = app.test_client()
    username = 'autotestuser'
    email = 'autotest@example.com'
    password = 'testpass123'

    resp = client.post('/register', data={
        'username': username,
        'email': email,
        'password': password,
    }, follow_redirects=True)

    print('Status code:', resp.status_code)
    text = resp.get_data(as_text=True)
    # Print a short slice of the response where flashes usually render
    if 'All fields are required' in text:
        print('Flash: All fields are required')
    if 'Username or Email already registered' in text:
        print('Flash: Username or Email already registered')

    # Check DB
    user = User.query.filter_by(username=username).first()
    print('User in DB:', bool(user))
    if user:
        print('User id/email:', user.id, user.email)
