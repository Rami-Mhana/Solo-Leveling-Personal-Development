# Quick Reference Guide

## Command Cheat Sheet

### Setup & Running
```powershell
# First time setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_db.py

# Run dev server
python run.py

# Run tests
python -u test\auth_flow_test.py
```

### Database
```powershell
# Reset database
python create_db.py

# Check database
sqlite3 instance/sololeveling.db
```

### Common Tasks
```python
# Check user progress
from app import create_app
from app.models import db, User
app = create_app()
with app.app_context():
    user = User.query.filter_by(username='testuser').first()
    print(user.get_progress())

# Award XP manually
user.xp += 100
db.session.commit()

# Check achievements
achievements = user.earned_achievements
for a in achievements:
    print(f"- {a.achievement_id} (unlocked {a.earned_at})")
```

---

## API Quick Reference

### Authentication Flow
```
POST /register {username, email, password}
  ↓
POST /login {username, password}
  ↓
GET / (dashboard)
  ↓
GET /logout
```

### Activity Flow
```
POST /complete-task {id}
  Response: { success, xp_gained, notifications, progress }

GET /api/progress
  Response: { level, xp, stats, achievements, ... }

GET /api/achievements
  Response: [{ id, earned_at }, ...]
```

### Quest Creation
```python
from app.models import Quest
quest = Quest(
    title='Learn Flask',
    description='Complete tutorial',
    difficulty='C',
    xp_reward=100,
    user_id=current_user.id
)
db.session.add(quest)
db.session.commit()
```

---

## File Quick Reference

| File | Purpose | Edit for... |
|------|---------|-------------|
| `app/models.py` | Data models | XP values, achievements, stats |
| `app/routes.py` | API endpoints | Activity types, logic |
| `app/helpers.py` | Business logic | Activity processing |
| `app/templates/dashboard.html` | Dashboard UI | Layout, display |
| `app/static/js/achievements.js` | Achievement logic | Unlock conditions |
| `config.py` | Settings | Database, secret key |
| `requirements.txt` | Dependencies | Package versions |

---

## Achievements Unlock Conditions

| Achievement | Condition |
|-------------|-----------|
| Beginner Hunter | Complete 1 quest |
| Dedicated Hunter | Complete 10 quests |
| Meditation Master | 7-day meditation streak |
| Bookworm | Read 5 books |
| Habit Former | Complete 20 habits |
| Goal Achiever | Achieve 5 goals |

---

## XP Reference

| Activity | XP |
|----------|-----|
| Complete Quest | 100 |
| Read Book | 150 |
| Achieve Goal | 200 |
| Meditate | 50 |
| Complete Habit | 30 |

---

## Level/Rank Reference

| Level | XP Required | Rank |
|-------|-------------|------|
| 1 | 0 | E-Rank |
| 2 | 1,000 | E-Rank |
| 3 | 2,500 | D-Rank |
| 4 | 5,000 | D-Rank |
| 5 | 8,000 | C-Rank |
| 6 | 12,000 | C-Rank |
| 7 | 17,000 | B-Rank |
| 8 | 23,000 | B-Rank |
| 9 | 30,000 | A-Rank |
| 10 | 38,000 | S-Rank |

---

## Troubleshooting Matrix

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError: app" | Activate venv: `.\.venv\Scripts\Activate.ps1` |
| "Port already in use" | Kill Flask: `lsof -ti:5000 \| xargs kill -9` |
| "No such table: quest" | Recreate DB: `python create_db.py` |
| No notifications | Check browser console, ensure sounds exist |
| XP not awarded | Check `/complete-task` response JSON |
| Achievement not unlocking | Check condition in `achievements.js` |

---

## Documentation Map

```
README.md                    ← Start here (quick start)
  ├→ ARCHITECTURE.md         (system design, API details)
  ├→ PROJECT_PLAN.md         (status, roadmap, issues)
  ├→ SESSION_SUMMARY.md      (what was built, retrospective)
  └→ QUICK_REFERENCE.md      (this file)
```

---

## Performance Tips

### Optimize Queries
```python
# Slow: N+1 query
for user in User.query.all():
    print(user.earned_achievements)  # Query per user!

# Fast: Eager load
User.query.options(db.joinedload('earned_achievements')).all()
```

### Cache Achievements
```python
# In helpers.py
ACHIEVEMENT_CACHE = {}
for ach in Achievement.query.all():
    ACHIEVEMENT_CACHE[ach.id] = ach
```

### Batch Inserts
```python
# Slow: Individual commits
for i in range(100):
    db.session.add(Item())
    db.session.commit()

# Fast: Batch commit
for i in range(100):
    db.session.add(Item())
db.session.commit()
```

---

## Security Checklist

- [x] Password hashing (Werkzeug)
- [x] Session management (Flask-Login)
- [x] CSRF protection on forms
- [ ] HTTPS/SSL (production)
- [ ] Rate limiting
- [ ] Input validation
- [ ] SQL injection protection (ORM)
- [ ] XSS protection (Jinja escaping)

---

## Debug Mode

### Enable Debug Output
```python
# In run.py
app.run(debug=True)

# Or from command line
FLASK_ENV=development FLASK_DEBUG=1 flask run
```

### Check Database State
```python
from app import create_app
from app.models import db, User
app = create_app()
with app.app_context():
    print(f"Users: {User.query.count()}")
    print(f"Quests: {Quest.query.count()}")
    print(f"Achievements: {len(User.query.first().earned_achievements)}")
```

### Monitor Requests
```python
# In app/__init__.py
from flask import request
import logging

@app.before_request
def log_request():
    logging.info(f"{request.method} {request.path}")
```

---

## Feature Flags (Future)

```python
# To add feature toggling:
FEATURES = {
    'SHOP_ENABLED': False,
    'LEADERBOARD_ENABLED': False,
    'SOCIAL_ENABLED': False,
}

@app.route('/shop')
def shop():
    if not FEATURES['SHOP_ENABLED']:
        abort(404)
    # ... shop logic
```

---

## Configuration Examples

### Development
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
DEBUG = True
TESTING = False
```

### Testing
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
DEBUG = True
TESTING = True
```

### Production
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
DEBUG = False
TESTING = False
```

---

## Common Git Commands

```bash
# View changes
git status
git diff

# Stage and commit
git add .
git commit -m "Feature: description"

# Push
git push origin master

# Create branch
git checkout -b feature/name
```

---

## Extension Points

### Add New Achievement
1. Define in `achievements.js` ACHIEVEMENTS object
2. Add condition check in `checkAchievements()`
3. Add unlock logic to `User.check_achievements()`

### Add New Activity Type
1. Add endpoint in `routes.py`
2. Add XP reward in `User.XP_REWARDS`
3. Call `update_stats()` and `process_activity()`
4. Add button to template
5. Wire in `completeActivity(type, id)`

### Add New Stat
1. Add column to User model
2. Add to dashboard stat bars
3. Add to profile stat display
4. Add condition to achievements

---

## Monitoring & Logging

### Basic Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Request Logging
```python
@app.after_request
def log_response(response):
    logging.info(f"{request.method} {request.path} - {response.status_code}")
    return response
```

---

**Last Updated**: November 26, 2025
