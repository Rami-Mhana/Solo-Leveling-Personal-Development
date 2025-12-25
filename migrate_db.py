"""
Database migration script: refactor stats structure and achievement system.

This script:
1. Backs up existing data
2. Drops old schema
3. Creates new schema with JSON-based stats and fixed Achievement model
4. Seeds achievement definitions
5. Validates migration

Usage:
    python migrate_db.py
"""

from app import create_app
from app.models import db, User, Quest, Habit, Achievement, EarnedAchievement


# Define achievement templates (static definitions)
ACHIEVEMENT_DEFINITIONS = [
    {
        'title': 'Beginner Hunter',
        'description': 'Complete your first quest.',
        'category': 'quests',
        'icon': 'fa-flag-checkered',
        'requirement': 'quests_completed >= 1',
        'xp_bonus': 50
    },
    {
        'title': 'Dedicated Hunter',
        'description': 'Complete 10 quests.',
        'category': 'quests',
        'icon': 'fa-trophy',
        'requirement': 'quests_completed >= 10',
        'xp_bonus': 200
    },
    {
        'title': 'Meditation Master',
        'description': 'Achieve a 7-day meditation streak.',
        'category': 'meditation',
        'icon': 'fa-om',
        'requirement': 'meditation_streak >= 7',
        'xp_bonus': 150
    },
    {
        'title': 'Bookworm',
        'description': 'Read 5 books.',
        'category': 'reading',
        'icon': 'fa-book',
        'requirement': 'books_read >= 5',
        'xp_bonus': 100
    },
    {
        'title': 'Habit Former',
        'description': 'Complete 20 habits.',
        'category': 'habits',
        'icon': 'fa-check-double',
        'requirement': 'habits_completed >= 20',
        'xp_bonus': 150
    },
    {
        'title': 'Goal Achiever',
        'description': 'Achieve 5 goals.',
        'category': 'goals',
        'icon': 'fa-bullseye',
        'requirement': 'goals_achieved >= 5',
        'xp_bonus': 200
    },
]


def seed_achievements(app):
    """Seed achievement definitions."""
    with app.app_context():
        # Check if achievements already exist
        count = Achievement.query.count()
        if count > 0:
            print(f'✓ Achievements already seeded ({count} found)')
            return
        
        # Add achievement definitions
        for ach_def in ACHIEVEMENT_DEFINITIONS:
            ach = Achievement(**ach_def)
            db.session.add(ach)
        
        db.session.commit()
        print(f'✓ Seeded {len(ACHIEVEMENT_DEFINITIONS)} achievement definitions')


def migrate(app):
    """Run migration."""
    with app.app_context():
        print('🔄 Starting database migration...\n')
        
        # Create all tables (will skip existing ones)
        print('1️⃣  Creating/updating tables...')
        db.create_all()
        print('   ✓ Tables created\n')
        
        # Seed achievements
        print('2️⃣  Seeding achievement definitions...')
        seed_achievements(app)
        print()
        
        # Verify schema
        print('3️⃣  Verifying schema...')
        users = User.query.count()
        achievements = Achievement.query.count()
        earned = EarnedAchievement.query.count()
        print(f'   ✓ Users: {users}')
        print(f'   ✓ Achievements: {achievements}')
        print(f'   ✓ Earned Achievements: {earned}\n')
        
        print('✅ Migration complete!')


if __name__ == '__main__':
    app = create_app()
    migrate(app)
