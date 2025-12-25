"""Test quest creation to identify and fix the bug."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, User, Quest


def test_quest_creation():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Create a test user
        u = User(username='testuser', email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        
        # Create test client
        client = app.test_client()
        
        # Login
        resp = client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
        print(f'Login status: {resp.status_code}')
        
        # Try creating a quest via /pd/tasks/new
        print('\n🔍 Testing POST /pd/tasks/new...')
        resp = client.post('/pd/tasks/new', json={
            'title': 'Learn Python',
            'description': 'Complete Python course',
            'difficulty': 'C',
            'quest_type': 'daily'
        })
        print(f'Status: {resp.status_code}')
        print(f'Response: {resp.get_json()}')
        
        # Check if quest was created
        quest = Quest.query.first()
        if quest:
            print(f'✅ Quest created: {quest.title}')
        else:
            print('❌ Quest was NOT created')
        
        # Also test the /complete-task endpoint
        print('\n🔍 Testing POST /complete-task...')
        if quest:
            resp = client.post('/complete-task', json={'id': quest.id})
            print(f'Status: {resp.status_code}')
            print(f'Response: {resp.get_json()}')


if __name__ == '__main__':
    test_quest_creation()
