from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.config.from_object('config.Config')

# --- Dummy Data (for initial practice without a database) ---
users = {} # {username: {'password': 'hashed_password', 'skills': {}, 'quests': []}}
current_user = None

# --- Routes ---
@app.route('/')
def index():
    global current_user
    if current_user:
        # Example data for the dashboard (replace with real data later)
        user_data = {
            'username': current_user,
            'level': 1,
            'xp': 150,
            'xp_to_next_level': 300,
            # Dictionary of skills with their levels and progress & Dictionary inside a dictoinary
            'skills': {
                'Coding': {'level': 5, 'xp': 200, 'progress': 75},
                'Cybersecurity': {'level': 3, 'xp': 80, 'progress': 50}
            },
            # List of active quests with their status 
            # Dictionary inside a list
            'active_quests': [
                {'title': 'Finish Flask Tutorial', 'xp_reward': 50, 'status': 'In Progress'},
                {'title': 'Read Python Docs', 'xp_reward': 20, 'status': 'Completed'},
            ]
        }
        return render_template('dashboard.html', user=user_data)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password: # In a real app, hash and verify passwords!
            current_user = username
            flash(f'Logged in as {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists', 'danger')
        else:
            users[username] = {'password': password, 'skills': {}, 'quests': []} # Store plain password for now, HASH LATER!
            flash(f'Account created for {username}. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    global current_user
    current_user = None
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Create dummy user for testing
    if not 'testuser' in users:
        users['testuser'] = {'password': 'password123', 'skills': {}, 'quests': []}
    
    app.run(host="0.0.0.0", port=5000, debug=True)
