"""Legacy/demo routes converted to a blueprint.

This module used to create a standalone Flask app. It's now a blueprint so it
can be registered with the central application factory in `app.__init__`.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

legacy_bp = Blueprint('legacy', __name__)

# --- Dummy Data (for initial practice without a database) ---
users = {}  # {username: {'password': 'hashed_password', 'skills': {}, 'quests': []}}


@legacy_bp.route('/')
def legacy_index():
    if 'username' in session:
        username = session['username']
        user_data = {
            'username': username,
            'level': 1,
            'xp': 150,
            'xp_to_next_level': 300,
            'skills': {
                'Coding': {'level': 5, 'xp': 200, 'progress': 75},
                'Cybersecurity': {'level': 3, 'xp': 80, 'progress': 50}
            },
            'active_quests': [
                {'title': 'Finish Flask Tutorial', 'xp_reward': 50, 'status': 'In Progress'},
                {'title': 'Read Python Docs', 'xp_reward': 20, 'status': 'Completed'},
            ]
        }
        return render_template('dashboard.html', user=user_data)
    # Redirect to the main blueprint's login page
    return redirect(url_for('main.login'))


@legacy_bp.route('/login', methods=['GET', 'POST'])
def legacy_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash(f'Logged in as {username}!', 'success')
            return redirect(url_for('legacy.legacy_index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


@legacy_bp.route('/register', methods=['GET', 'POST'])
def legacy_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            flash('Username already exists', 'danger')
        else:
            users[username] = {'password': password, 'skills': {}, 'quests': []}
            flash(f'Account created for {username}. Please log in.', 'success')
            return redirect(url_for('legacy.legacy_login'))
    return render_template('register.html')


@legacy_bp.route('/logout')
def legacy_logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('legacy.legacy_index'))