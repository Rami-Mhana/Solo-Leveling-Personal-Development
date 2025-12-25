from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Solo Levelling / Character Progression
    level = db.Column(db.Integer, default=1)
    rank = db.Column(db.String(50), default='E-Rank Hunter')
    xp = db.Column(db.Integer, default=0)
    
    # Core Stats (System-defined: 5 base stats that grow with leveling)
    # Stored as JSON for flexibility
    core_stats = db.Column(db.JSON, default=lambda: {
        'strength': 10,
        'intelligence': 10,
        'agility': 10,
        'willpower': 10,
        'discipline': 10
    })
    
    # Player Stats (User-defined: personal development metrics)
    # Stored as JSON for flexibility
    player_stats = db.Column(db.JSON, default=lambda: {
        'meditation_streak': 0,
        'books_read': 0,
        'habits_completed': 0,
        'goals_achieved': 0,
        'quests_completed': 0
    })
    
    # Relationships
    # 'Achievement' model holds achievement definitions; EarnedAchievement tracks which user earned which achievement
    earned_achievements = db.relationship('EarnedAchievement', backref='user', lazy=True)

    # XP Constants
    XP_REWARDS = {
        'COMPLETE_QUEST': 100,
        'MEDITATION_DAILY': 50,
        'READ_BOOK': 150,
        'COMPLETE_HABIT': 30,
        'ACHIEVE_GOAL': 200
    }

    # Level Thresholds
    LEVEL_THRESHOLDS = [
        0,      # Level 1
        1000,   # Level 2
        2500,   # Level 3
        5000,   # Level 4
        8000,   # Level 5
        12000,  # Level 6
        17000,  # Level 7
        23000,  # Level 8
        30000,  # Level 9
        38000   # Level 10
    ]

    # Hunter Ranks
    HUNTER_RANKS = {
        1: 'E-Rank Hunter',
        3: 'D-Rank Hunter',
        5: 'C-Rank Hunter',
        7: 'B-Rank Hunter',
        9: 'A-Rank Hunter',
        10: 'S-Rank Hunter'
    }
    
    # Backward compatibility properties for core stats
    @property
    def strength(self):
        return self.core_stats.get('strength', 10)
    
    @property
    def intelligence(self):
        return self.core_stats.get('intelligence', 10)
    
    @property
    def agility(self):
        return self.core_stats.get('agility', 10)
    
    @property
    def willpower(self):
        return self.core_stats.get('willpower', 10)
    
    @property
    def discipline(self):
        return self.core_stats.get('discipline', 10)
    
    # Backward compatibility properties for player stats
    @property
    def meditation_streak(self):
        return self.player_stats.get('meditation_streak', 0)
    
    @property
    def books_read(self):
        return self.player_stats.get('books_read', 0)
    
    @property
    def habits_completed(self):
        return self.player_stats.get('habits_completed', 0)
    
    @property
    def goals_achieved(self):
        return self.player_stats.get('goals_achieved', 0)
    
    @property
    def quests_completed(self):
        return self.player_stats.get('quests_completed', 0)
    
    # Password hashing and verification
    def set_password(self, password):
        """Hashes the password and sets it to the password_hash attribute."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def add_xp(self, activity_type):
        """Add XP for an activity and check for level up."""
        if activity_type in self.XP_REWARDS:
            old_level = self.level
            self.xp += self.XP_REWARDS[activity_type]
            
            # Check for level up
            for level, threshold in enumerate(self.LEVEL_THRESHOLDS):
                if self.xp >= threshold:
                    self.level = level + 1 # level-up to next level.
            
            # Check for rank update if leveled up
            if self.level > old_level: # The relationship between the level & rank
                self._update_rank()

                
            db.session.commit()
            return { # A dictionary to indicate level up status
                'leveledUp': self.level > old_level,
                'newLevel': self.level,
                'newRank': self.rank if self.level > old_level else None
            }
        return None

    def _update_rank(self):
        """Update the hunter rank based on current level."""
        for req_level, rank in sorted(self.HUNTER_RANKS.items(), reverse=True):
            if self.level >= req_level:
                self.rank = rank
                break

    def check_achievements(self):
        """Check for new achievements and return any that were earned."""
        earned = []
        
        # Achievement unlock conditions mapped to their titles
        conditions = {
            'Beginner Hunter': self.quests_completed >= 1,
            'Dedicated Hunter': self.quests_completed >= 10,
            'Meditation Master': self.meditation_streak >= 7,
            'Bookworm': self.books_read >= 5,
            'Habit Former': self.habits_completed >= 20,
            'Goal Achiever': self.goals_achieved >= 5,
        }
        
        # Check each condition and add achievement if earned
        for title, condition_met in conditions.items():
            if condition_met:
                ach = Achievement.query.filter_by(title=title).first()
                if ach:
                    result = self._add_achievement(ach.id)
                    if result:
                        earned.append(title)
        
        return earned

    def _add_achievement(self, achievement_id):
        """Add an achievement if not already earned."""
        existing = EarnedAchievement.query.filter_by(
            user_id=self.id,
            achievement_id=achievement_id
        ).first()

        if not existing:
            earned = EarnedAchievement(
                user_id=self.id,
                achievement_id=achievement_id
            )
            db.session.add(earned)
            db.session.commit()
            # Return the achievement ID for logging
            return achievement_id
        return None

    def get_progress(self):
        """Get the user's current progress data for frontend display."""
        next_level_xp = self.LEVEL_THRESHOLDS[self.level] if self.level < len(self.LEVEL_THRESHOLDS) else float('inf')
        current_level_xp = self.LEVEL_THRESHOLDS[self.level - 1] if self.level > 0 else 0
        
        return {
            'level': self.level,
            'rank': self.rank,
            'xp': self.xp,
            'xp_progress': (self.xp - current_level_xp) / (next_level_xp - current_level_xp) * 100,
            'xp_needed': next_level_xp - self.xp,
            'stats': {
                'strength': self.strength,
                'intelligence': self.intelligence,
                'agility': self.agility,
                'willpower': self.willpower,
                'discipline': self.discipline
            },
            'progress': {
                'meditation_streak': self.meditation_streak,
                'books_read': self.books_read,
                'habits_completed': self.habits_completed,
                'goals_achieved': self.goals_achieved,
                'quests_completed': self.quests_completed
            },
            'achievements': [
                {
                    'id': achievement.achievement_id,
                    'earned_at': achievement.earned_at.isoformat()
                }
                for achievement in self.earned_achievements
            ]
        }

    def __repr__(self):
        return f'<User {self.username}>'

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(50))  # E, D, C, B, A, S
    xp_reward = db.Column(db.Integer)
    quest_type = db.Column(db.String(50))  # daily, weekly, achievement
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('quests', lazy=True))

class Achievement(db.Model):
    __tablename__ = 'achievement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # fitness, reading, meditation, etc.
    icon = db.Column(db.String(200))
    requirement = db.Column(db.Text)
    xp_bonus = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Achievement definitions are global, not user-specific
    # EarnedAchievement handles the many-to-many relationship with User
 

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(50))  # daily, weekly, monthly
    current_streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_completed = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('habits', lazy=True))


class EarnedAchievement(db.Model):
    __tablename__ = 'earned_achievement'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    achievement = db.relationship('Achievement', backref='earned_by')

