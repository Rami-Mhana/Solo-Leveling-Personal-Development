# Solo Leveling Personal Development

A gamified personal development Flask web application inspired by the Solo Leveling anime. Track quests, build habits, and progress through a leveling system with achievements.

**Current Status**: 🟢 **Functional** — Core features working, ready for extended use

---

## Quick Start

### Prerequisites
- Python 3.8+
- PowerShell (or Bash)

### Setup (Windows PowerShell)

```powershell
# 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python create_db.py

# 4. Run development server
python run.py
```

Open http://127.0.0.1:5000 in your browser. Login with seeded user:
- **Username**: `testuser`
- **Password**: `password`

---

## Features

### 🎮 Core Gamification
- **XP System**: Earn XP by completing quests, reading books, meditating, building habits
- **Leveling**: 10-level progression (0 → 38,000 XP) with milestone rewards
- **Hunter Ranks**: E-Rank (novice) → S-Rank (master) based on level
- **Achievements**: 6+ unlockable achievements for reaching milestones
- **Character Stats**: 5 core stats (Strength, Intelligence, Agility, Willpower, Discipline)

### 📊 Personal Development
- **Quest System**: Create, track, and complete personal goals
- **Habit Tracking**: Build recurring habits with streak counters
- **Activity Logging**: Log meditation sessions, books read, goals achieved
- **Progress Visualization**: Real-time XP bars and stat progress

### 👤 User Management
- **Authentication**: Secure registration & login
- **Profile**: View and edit profile information
- **Dashboard**: Central hub for all activities
- **Progress API**: JSON endpoints for frontend integration

### 🎨 UI/UX
- **Dark Gaming Theme**: Neon purple, pink gradient accents
- **Responsive Design**: Works on desktop and mobile
- **Real-Time Notifications**: Achievement unlocks, level-ups with sound
- **Animations**: Smooth transitions and particle effects
- **Sidebar Navigation**: Gaming-inspired menu with XP display

---

## Key Endpoints

### Authentication
- `GET/POST /login` — User login
- `GET/POST /register` — User registration
- `GET /logout` — End session

### Dashboard & Profile
- `GET /` — Main dashboard (requires login)
- `GET/POST /profile` — View/edit profile (requires login)

### Activities (Require Login)
- `POST /complete-task` — Mark quest complete, award XP
- `POST /update-meditation` — Log meditation session
- `POST /complete-book` — Mark book as read
- `POST /complete-habit` — Log habit completion
- `POST /achieve-goal` — Mark goal achieved

### API
- `GET /api/progress` — Current user progress (JSON)
- `GET /api/achievements` — User's earned achievements (JSON)

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask 3.1.2 |
| ORM | SQLAlchemy 2.0.43 |
| Database | SQLite (dev), PostgreSQL (prod) |
| Auth | Flask-Login 0.6.3 |
| Frontend CSS | Tailwind CSS (CDN) |
| Frontend JS | Alpine.js + Vanilla JS |
| Templates | Jinja2 |
| Security | Werkzeug (hashing) |

---

## Project Structure

```
app/
├── __init__.py           # Application factory
├── models.py             # SQLAlchemy ORM models
├── helpers.py            # Business logic
├── routes.py             # Activity & API endpoints
├── main_routes.py        # Authentication & dashboard
├── static/
│   ├── css/style.css     # Custom styling
│   ├── js/achievements.js # Achievement system
│   └── sounds/           # Audio assets
└── templates/            # Jinja2 templates

config.py                # Flask configuration
create_db.py            # Database initialization
run.py                  # Development server
test/                   # Test suite
```

---

## Development

### Running Tests
```powershell
python -u test\auth_flow_test.py
# Result: ALL TESTS PASSED
```

### Checking User Progress
```python
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='testuser').first()
    progress = user.get_progress()
    print(f"Level: {progress['level']}, XP: {progress['xp']}")
```

---

## Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** — System design, data models, API details
- **[PROJECT_PLAN.md](./PROJECT_PLAN.md)** — Current status, roadmap, known issues

---

## Known Limitations

1. SQLite for dev, PostgreSQL needed for production
2. Single-player only (no multiplayer yet)
3. No email verification
4. No password reset functionality
5. Limited achievements (easily expandable)

---

## Roadmap

### Phase 1: Stability ✅
- [x] Core gamification
- [x] Achievement tracking
- [x] Authentication
- [x] Dashboard UI

### Phase 2: Features (Current)
- [ ] Sound assets
- [ ] DB migrations
- [ ] Expanded achievements
- [ ] Reward shop

### Phase 3: Quality
- [ ] Full test coverage
- [ ] Error handling
- [ ] Performance optimization

---

**Last Updated**: November 26, 2025  
**Status**: 🟢 Ready for development | ⚠️ Not production-ready
