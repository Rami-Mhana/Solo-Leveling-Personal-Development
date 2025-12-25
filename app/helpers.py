from flask import jsonify
from .models import db, User, Achievement

def process_activity(user, activity_type):
    """Process an activity for a user, handling XP, achievements, and level ups."""
    # Add XP and check for level up
    level_info = user.add_xp(activity_type)
    
    # Check for new achievements
    new_achievements = user.check_achievements()
    
    # Prepare response data
    response = {
        'success': True,
        'notifications': []
    }
    
    # Add level up notification if applicable
    if level_info and level_info['leveledUp']:
        response['notifications'].append({
            'type': 'levelup',
            'message': f"Advanced to Level {level_info['newLevel']}!",
            'details': {
                'level': level_info['newLevel'],
                'rank': level_info['newRank']
            }
        })
    
    # Add achievement notifications
    for achievement_id in new_achievements:
        response['notifications'].append({
            'type': 'achievement',
            'message': f"Achievement Unlocked: {achievement_id}!",
            'achievement': achievement_id
        })
    
    # Get updated progress data
    response['progress'] = user.get_progress()
    
    return jsonify(response)

def update_stats(user, stat_updates):
    """Update user stats and process achievements."""
    for stat, value in stat_updates.items():
        if hasattr(user, stat):
            setattr(user, stat, getattr(user, stat) + value)
    
    db.session.commit()
    
    # Check for achievements and get progress
    new_achievements = user.check_achievements()
    progress = user.get_progress()
    
    return {
        'achievements': new_achievements,
        'progress': progress
    }