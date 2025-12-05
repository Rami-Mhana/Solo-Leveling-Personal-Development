from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Quest, db  # Import the models and db object

# Create the Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def index():
    """Home page route."""
    return render_template('index.html', title='Home')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Simple validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html', title='Register')

        # Check if user already exists
        user_check = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_check:
            flash('Username or Email already registered.', 'danger')
            return render_template('register.html', title='Register')

        # Create and save new user to SQLAlchemy .db file
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password

        db.session.add(new_user)
        db.session.commit()

        # Auto-login the new user for convenience
        login_user(new_user)
        flash(f'Welcome, {username}! Your account was created.', 'success')
        return redirect(url_for('main.dashboard'))

    # GET -> render registration page
    return render_template('register.html', title='Register')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            from flask_login import login_user
            login_user(user)
            flash(f'Welcome back, {username}! Ready to continue your journey?', 'success')
            
            # Redirect to the next page if it exists, otherwise go to dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password. Try again!', 'danger')

    return render_template('login.html', title='Login')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route."""
    # Use current_user data from Flask-Login
    user_data = {
        'username': current_user.username,
        'level': current_user.level,
        'xp': current_user.xp,
        'rank': current_user.rank,
        'strength': current_user.strength,
        'intelligence': current_user.intelligence,
        'agility': current_user.agility,
        'willpower': current_user.willpower,
        'discipline': current_user.discipline
    }
    
    # Get active quests for the user
    quests = Quest.query.filter_by(user_id=current_user.id, completed=False).limit(5).all()
    
    return render_template('dashboard.html', user=user_data, quests=quests, title='Dashboard')

@main_bp.route('/logout')
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash('You have been successfully logged out. Come back stronger!', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/market')
def market():
    """Market/shop route placeholder."""
    return "Market Page - Coming Soon!"

@main_bp.route('/player_info')
@login_required
def player_status():
    """Player Status route to render a compact and useful player status view.

    Keeps labels and clean tables, removes dump/sample data and exposes only
    relevant information from the logged-in user's stats and progress.
    """
    # Safely gather stats (core_stats and player_stats are JSON columns)
    core = current_user.core_stats or {}
    player = current_user.player_stats or {}

    # Basic activity counters
    active_quests = Quest.query.filter_by(user_id=current_user.id, completed=False).count()
    total_quests = Quest.query.filter_by(user_id=current_user.id).count()
    achievements_count = len(current_user.earned_achievements or [])

    stats = {
        'core': {
            'strength': core.get('strength', 0),
            'intelligence': core.get('intelligence', 0),
            'agility': core.get('agility', 0),
            'willpower': core.get('willpower', 0),
            'discipline': core.get('discipline', 0)
        },
        'player': {
            'meditation_streak': player.get('meditation_streak', 0),
            'books_read': player.get('books_read', 0),
            'habits_completed': player.get('habits_completed', 0),
            'goals_achieved': player.get('goals_achieved', 0),
            'quests_completed': player.get('quests_completed', 0)
        },
        'level': current_user.level,
        'xp': current_user.xp,
        'rank': current_user.rank,
        'active_quests': active_quests,
        'total_quests': total_quests,
        'achievements_count': achievements_count
    }

    return render_template('player_status.html', title='Player Status', stats=stats)

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and edit current user's profile."""
    if request.method == 'POST':
        # Update allowed fields: username, email, optional password
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Basic validation
        if not username or not email:
            flash('Username and email are required.', 'danger')
            return redirect(url_for('main.profile'))

        # Check uniqueness when changed
        if username != current_user.username:
            if User.query.filter_by(username=username).first():
                flash('Username already taken.', 'danger')
                return redirect(url_for('main.profile'))

        if email != current_user.email:
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'danger')
                return redirect(url_for('main.profile'))

        # Apply changes
        current_user.username = username
        current_user.email = email
        if password:
            current_user.set_password(password)

        db.session.add(current_user)
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('main.profile'))

    # GET -> render profile page
    return render_template('profile.html', title='Your Profile')


@main_bp.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    print('Initialized the database at sololeveling.db.')