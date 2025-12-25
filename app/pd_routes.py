from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Quest, Achievement, Habit, User
from datetime import datetime, timedelta

pd_bp = Blueprint('pd', __name__)

@pd_bp.route('/tasks')
def tasks():
    """List all personal development tasks."""
    # Get the current user's quests
    daily_quests = Quest.query.filter_by(user_id=current_user.id, quest_type='daily').all() if current_user.is_authenticated else []
    weekly_quests = Quest.query.filter_by(user_id=current_user.id, quest_type='weekly').all() if current_user.is_authenticated else []
    achievement_quests = Quest.query.filter_by(user_id=current_user.id, quest_type='achievement').all() if current_user.is_authenticated else []
    
    return render_template('tasks.html',
                         daily_quests=daily_quests,
                         weekly_quests=weekly_quests,
                         achievement_quests=achievement_quests)

@pd_bp.route('/tasks/new', methods=['POST'])
@login_required
def create_task():
    """Create a new personal development task."""
    data = request.json
    
    new_quest = Quest(
        title=data['title'],
        description=data['description'],
        difficulty=data['difficulty'],
        xp_reward=calculate_xp_reward(data['difficulty']),
        quest_type=data['quest_type'],
        deadline=datetime.strptime(data['deadline'], '%Y-%m-%d') if 'deadline' in data else None,
        user_id=current_user.id
    )
    
    db.session.add(new_quest)
    db.session.commit()
    
    return jsonify({'message': 'Task created successfully!', 'quest_id': new_quest.id})

@pd_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    """Mark a task as complete and award XP."""
    quest = Quest.query.get_or_404(task_id)
    user = current_user
    
    if quest.completed:
        return jsonify({'message': 'Task already completed!'})
    
    # Mark quest as complete
    quest.completed = True
    
    # Award XP to user
    user.xp += quest.xp_reward
    
    # Check for level up
    new_level = calculate_level(user.xp)
    if new_level > user.level:
        user.level = new_level
        flash(f'Congratulations! You reached level {new_level}!', 'success')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Task completed successfully!',
        'xp_gained': quest.xp_reward,
        'new_total_xp': user.xp,
        'level': user.level
    })

@pd_bp.route('/habits')
@login_required
def habits():
    """Display user's habits and streaks."""
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template('habits.html', habits=habits)

@pd_bp.route('/habits/track', methods=['POST'])
def track_habit():
    """Track a habit completion."""
    data = request.json
    habit = Habit.query.get_or_404(data['habit_id'])
    
    # Update streak
    if not habit.last_completed or \
       habit.last_completed.date() < datetime.utcnow().date() - timedelta(days=1):
        habit.current_streak = 1
    else:
        habit.current_streak += 1
    
    # Update best streak if current is higher
    if habit.current_streak > habit.best_streak:
        habit.best_streak = habit.current_streak
    
    habit.last_completed = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Habit tracked successfully!',
        'current_streak': habit.current_streak,
        'best_streak': habit.best_streak
    })


@pd_bp.route('/stats', methods=['GET'])
@login_required
def stats():
    """Render a simple stats management page where player-defined stats can be viewed.
    Core system stats are displayed read-only; player stats can be updated via the API.
    """
    # Show current stats (player can edit their player_stats)
    core = current_user.core_stats or {}
    player = current_user.player_stats or {}
    return render_template('pd_stats.html', core=core, player=player)


@pd_bp.route('/stats/update', methods=['POST'])
@login_required
def update_stats():
    """Update player-defined stats. Accepts JSON payload with keys for player_stats.

    Example JSON: { "meditation_streak": 3, "books_read": 2 }
    """
    data = request.get_json() or {}
    # Only accept known player stat keys to avoid accidental injection
    allowed = {'meditation_streak', 'books_read', 'habits_completed', 'goals_achieved', 'quests_completed'}
    player = current_user.player_stats or {}

    changed = False
    for k, v in data.items():
        if k in allowed:
            try:
                player[k] = int(v)
            except Exception:
                player[k] = v
            changed = True

    if changed:
        current_user.player_stats = player
        db.session.add(current_user)
        db.session.commit()
        return jsonify({'success': True, 'player_stats': current_user.player_stats})

    return jsonify({'success': False, 'message': 'No valid fields provided.'}), 400

def calculate_xp_reward(difficulty):
    """Calculate XP reward based on task difficulty."""
    xp_map = {
        'E': 50,
        'D': 100,
        'C': 200,
        'B': 350,
        'A': 500,
        'S': 1000
    }
    return xp_map.get(difficulty.upper(), 100)

def calculate_level(xp):
    """Calculate level based on total XP."""
    # Each level requires base_xp * level_multiplier * current_level XP
    base_xp = 1000
    level_multiplier = 1.5
    
    level = 1
    xp_required = base_xp
    
    while xp >= xp_required:
        level += 1
        xp_required = int(base_xp * (level_multiplier ** (level - 1)))
    
    return level