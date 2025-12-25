"""
Final Route Testing & Validation Script
Tests all critical routes and functionality
"""

import sys
from app import create_app
from app.models import db, User

def test_route_registration():
    """Test that all routes are properly registered."""
    app = create_app()
    
    critical_routes = [
        '/',
        '/login',
        '/register',
        '/dashboard',
        '/profile',
        '/skills',
        '/api/skills/nodes',
        '/daily-report',
        '/player_info',
        '/complete-task',
    ]
    
    with app.app_context():
        registered_routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        for route in critical_routes:
            if route in registered_routes:
                print(f"[OK] {route}")
            else:
                print(f"[FAIL] {route} NOT FOUND")
                return False
    
    return True


def test_database_setup():
    """Test that all database tables exist."""
    app = create_app()
    
    required_tables = [
        'user',
        'quest',
        'achievement',
        'earned_achievement',
        'skill',
        'skill_node',
        'node_dependency',
        'daily_report',
        'quest_priority',
    ]
    
    with app.app_context():
        tables = db.inspect(db.engine).get_table_names()
        
        for table in required_tables:
            if table in tables:
                print(f"[OK] {table}")
            else:
                print(f"[FAIL] {table} NOT FOUND")
                return False
    
    return True


def test_user_model():
    """Test User model attributes."""
    app = create_app()
    
    with app.app_context():
        test_user = User(
            username='testuser',
            email='test@example.com'
        )
        
        attrs = [
            'username',
            'email',
            'level',
            'xp',
            'rank',
            'strength',
            'intelligence',
            'agility',
            'willpower',
            'discipline',
            'streak_count',
            'last_active_date',
            'streak_freeze_inventory',
        ]
        
        for attr in attrs:
            if hasattr(test_user, attr):
                print(f"[OK] {attr}")
            else:
                print(f"[FAIL] {attr} NOT FOUND")
                return False
        
    return True


def test_database_query():
    """Test that database queries work correctly."""
    app = create_app()
    
    with app.app_context():
        try:
            # Test basic query
            result = db.session.execute(db.text('SELECT COUNT(*) FROM user'))
            user_count = result.scalar()
            print(f"[OK] Database query works (users: {user_count})")
            
            # Test user retrieval
            if user_count > 0:
                user = User.query.first()
                print(f"[OK] User retrieval works")
                print(f"    - Username: {user.username}")
                print(f"    - Level: {user.level}")
                print(f"    - Streak Freezes: {user.streak_freeze_inventory}")
            
            return True
        except Exception as e:
            print(f"[FAIL] Database query error: {e}")
            return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("SOLO LEVELING LMS - FINAL TESTING".center(70))
    print("="*70)
    
    tests = [
        ("Route Registration", test_route_registration),
        ("Database Tables", test_database_setup),
        ("User Model", test_user_model),
        ("Database Queries", test_database_query),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}")
        print("-" * 70)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"[FAIL] ERROR in {name}: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status:8} | {name}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed\n")
    
    if passed == total:
        print("*** ALL TESTS PASSED! System is ready for deployment. ***\n")
        return 0
    else:
        print(f"*** {total - passed} test(s) failed. ***\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
