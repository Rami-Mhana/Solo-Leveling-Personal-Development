from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Achievement, Quest
from .helpers import process_activity, update_stats
from werkzeug.security import generate_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        # Provide templates that expect `user` and `quests`
        user = current_user
        # active quests for dashboard
        quests = Quest.query.filter_by(user_id=current_user.id, completed=False).all()
        return render_template('dashboard.html', user=user, quests=quests)
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            flash('Welcome back, Hunter!', 'success')
            return redirect(url_for('main.index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('register.html')
            
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your hunter account has been created! Please log in.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username is taken by another user
        if username != current_user.username:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already taken', 'danger')
                return redirect(url_for('main.profile'))
        
        # Check if email is taken by another user
        if email != current_user.email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered', 'danger')
                return redirect(url_for('main.profile'))
        
        # Update user information
        current_user.username = username
        current_user.email = email
        if password:
            current_user.set_password(password)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        
        return redirect(url_for('main.profile'))
        
    return render_template('profile.html')

@main_bp.route('/complete-task', methods=['POST'])
@login_required
def complete_task():
    """Handle task completion and reward XP."""
    task_id = request.form.get('id') or (request.json and request.json.get('id'))
    if not task_id:
        return jsonify({'success': False, 'message': 'Missing task id'}), 400

    quest = Quest.query.get(task_id)
    if not quest or quest.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Quest not found'}), 404

    if quest.completed:
        return jsonify({'success': False, 'message': 'Quest already completed'}), 400

    # Mark quest complete and award its XP
    quest.completed = True
    prev_level = current_user.level
    current_user.xp = (current_user.xp or 0) + (quest.xp_reward or 0)

    # Recalculate level based on thresholds defined on the model
    new_level = prev_level
    for idx, threshold in enumerate(current_user.LEVEL_THRESHOLDS):
        if current_user.xp >= threshold:
            new_level = idx + 1

    leveled_up = False
    if new_level > prev_level:
        current_user.level = new_level
        current_user._update_rank()
        leveled_up = True

    db.session.commit()

    # Check achievements
    new_achievements = current_user.check_achievements()

    notifications = []
    if leveled_up:
        notifications.append({
            'type': 'levelup',
            'message': f'Advanced to Level {current_user.level}!',
            'details': {'level': current_user.level, 'rank': current_user.rank}
        })

    for ach in new_achievements:
        notifications.append({
            'type': 'achievement',
            'message': f'Achievement Unlocked: {ach}!'
        })

    return jsonify({
        'success': True,
        'message': 'Quest completed successfully!',
        'xp_gained': quest.xp_reward,
        'notifications': notifications,
        'progress': current_user.get_progress()
    })

@main_bp.route('/update-meditation', methods=['POST'])
@login_required
def update_meditation():
    """Update meditation streak."""
    # Update meditation via helper (avoids double increments)
    result = update_stats(current_user, {'meditation_streak': 1})
    return process_activity(current_user, 'MEDITATION_DAILY')

@main_bp.route('/complete-book', methods=['POST'])
@login_required
def complete_book():
    """Mark a book as read."""
    result = update_stats(current_user, {'books_read': 1})
    return process_activity(current_user, 'READ_BOOK')

@main_bp.route('/complete-habit', methods=['POST'])
@login_required
def complete_habit():
    """Complete a daily habit."""
    result = update_stats(current_user, {'habits_completed': 1})
    return process_activity(current_user, 'COMPLETE_HABIT')

@main_bp.route('/achieve-goal', methods=['POST'])
@login_required
def achieve_goal():
    """Mark a goal as achieved."""
    result = update_stats(current_user, {'goals_achieved': 1})
    return process_activity(current_user, 'ACHIEVE_GOAL')

# API endpoints for frontend updates
@main_bp.route('/api/progress')
@login_required
def get_progress():
    """Get current user progress data."""
    return jsonify(current_user.get_progress())

@main_bp.route('/api/achievements')
@login_required
def get_achievements():
    """Get user achievements."""
    achievements = [
        {
            'id': achievement.achievement_id,
            'earned_at': achievement.earned_at.isoformat()
        }
        for achievement in current_user.earned_achievements
    ]
    return jsonify(achievements)
