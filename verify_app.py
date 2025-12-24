"""Test Flask app initialization"""
from app import create_app
from app.models import db

app = create_app()

print('Flask App Initialization Test')
print('='*50)

try:
    with app.app_context():
        # Test database connection
        result = db.session.execute(db.text('SELECT 1'))
        print('✓ Database connection: OK')
        
        # Test URL map
        routes = len([r for r in app.url_map.iter_rules()])
        print(f'✓ Total routes registered: {routes}')
        
        # Test blueprints
        blueprints = list(app.blueprints.keys())
        print(f'✓ Blueprints: {", ".join(blueprints)}')
        
        print()
        print('Flask app is ready to run!')
        print('Start the app with: python run.py')
        print('Then navigate to: http://127.0.0.1:5000')
        
except Exception as e:
    print(f'✗ Error: {e}')
    exit(1)
