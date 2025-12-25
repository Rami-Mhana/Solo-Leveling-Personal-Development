# Solo Leveling: Personal Development Gamified Platform

Transform your personal growth journey into an epic adventure inspired by the *Solo Leveling* anime! Track quests, build habits, level up through achievements, and gamify your path to self-improvement.

---

## 🎮 Quick Start

### Prerequisites
- Python 3.9+
- pip or poetry

### Installation

```bash
# Clone the repository
git clone https://github.com/Rami-Mhana/Solo-Leveling-Personal-Development.git
cd "Solo Leveling & Personal Development"

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate      # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run database migration
python migrate_db.py

# Start the development server
python run.py
```

Visit `http://localhost:5000` in your browser. The app will greet you with a login page.

---

## 📋 Default Credentials (Dev)

When you run the app for the first time, you can register a new account or use:
- **Username**: `testuser`
- **Password**: `password`

(Only available after running `create_db.py`)

---

## 🕹️ Core Features

### 🔐 Authentication
- Register a new hunter account
- Secure login/logout
- Profile management

### ⚡ Gamification System
- **XP & Leveling**: Earn XP from quest completions, meditation, reading, and habits
- **10-Level Progression**: From E-Rank Hunter to S-Rank Hunter
- **5 Core Stats**: Strength, Intelligence, Agility, Willpower, Discipline
- **Player Metrics**: Meditation streaks, books read, habits completed, goals achieved, quests completed

### 🎯 Quests & Tasks
- Create personal development quests
- Difficulty ratings (E-Rank through S-Rank)
- Track completion and earn rewards
- Organize by type: Daily, Weekly, Achievement

### 🏆 Achievement System
- 6+ achievements to unlock
- Unlock conditions based on player progress
- Automatic achievement detection
- XP bonuses for milestones

### 📚 Learn & Explore (NEW!)
- Curated quotes for motivation
- Learning approaches (5-Hour Rule, Atomic Habits, Deep Work, Pomodoro, Deliberate Practice)
- Patterns & principles (80/20 Rule, Systems Thinking, Compounding Effect)
- Personal development rules for success
- Interactive tab-based interface

### 🎨 Dark Gaming UI
- Neon purple/pink aesthetic
- Responsive sidebar navigation
- Real-time notifications
- Smooth animations and transitions

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask 3.1.2 |
| **Database** | SQLAlchemy 2.0 (SQLite/PostgreSQL) |
| **Auth** | Flask-Login 0.6.3 |
| **Frontend** | Jinja2, Tailwind CSS, Alpine.js |
| **Security** | Werkzeug (password hashing) |

---

## 📊 Data Model

### Core Entities

```
User (hunter)
├─ Core Stats (JSON): strength, intelligence, agility, willpower, discipline
├─ Player Stats (JSON): meditation_streak, books_read, habits_completed, goals_achieved, quests_completed
├─ Progression: level, rank, xp, created_at
├─ Relationships:
│  ├─ Quest (1:N) — tasks/goals
│  ├─ Habit (1:N) — recurring activities
│  └─ EarnedAchievement (1:N) → Achievement
│
Quest
├─ title, description, difficulty
├─ xp_reward, quest_type (daily/weekly/achievement)
├─ deadline, completed status
└─ FK: user_id

Achievement (global definitions)
├─ title, description, category, icon
├─ requirement, xp_bonus
└─ EarnedAchievement (tracks user unlocks)

Habit
├─ title, description, frequency
├─ current_streak, best_streak
├─ last_completed
└─ FK: user_id
```

---

## 🚀 API Endpoints

### Authentication
- `POST /register` — Create account
- `POST /login` — Authenticate user
- `GET /logout` — End session

### Dashboard & Profile
- `GET /` or `/dashboard` — Main dashboard
- `GET /profile` — View profile
- `POST /profile` — Update profile

### Personal Development (`/pd`)
- `GET /pd/tasks` — List quests
- `POST /pd/tasks/new` — Create quest
- `POST /pd/tasks/<id>/complete` — Complete quest

### Learning (`/learn`) **NEW**
- `GET /learn/` — Main learning hub
- `GET /learn/quotes` — Inspirational quotes
- `GET /learn/approaches` — Learning methodologies
- `GET /learn/patterns` — Principles & patterns
- `GET /learn/rules` — Personal dev rules

### Activities
- `POST /complete-task` — Mark task complete
- `POST /update-meditation` — Log meditation
- `POST /complete-book` — Mark book read
- `POST /complete-habit` — Log habit
- `POST /achieve-goal` — Mark goal achieved

### Data APIs
- `GET /api/progress` — Current progress (JSON)
- `GET /api/achievements` — Earned achievements (JSON)

---

## 📈 Achievement Progression

| Achievement | Condition | XP Bonus |
|------------|-----------|----------|
| Beginner Hunter | Complete 1st quest | 50 |
| Dedicated Hunter | Complete 10 quests | 200 |
| Meditation Master | 7-day streak | 150 |
| Bookworm | Read 5 books | 100 |
| Habit Former | Complete 20 habits | 150 |
| Goal Achiever | Achieve 5 goals | 200 |

---

## 🎓 XP System

| Activity | XP Reward |
|----------|-----------|
| Complete Quest | 100 |
| Daily Meditation | 50 |
| Read Book | 150 |
| Complete Habit | 30 |
| Achieve Goal | 200 |

### Level Thresholds

```
Level 1: 0 XP         (E-Rank Hunter)
Level 2: 1,000 XP     (E-Rank Hunter)
Level 3: 2,500 XP     (D-Rank Hunter)
Level 5: 8,000 XP     (C-Rank Hunter)
Level 7: 17,000 XP    (B-Rank Hunter)
Level 9: 30,000 XP    (A-Rank Hunter)
Level 10: 38,000 XP   (S-Rank Hunter)
```

---

## 🔧 Configuration

### Environment Variables

```bash
# .env (optional)
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/sololeveling.db
```

### Config File (`config.py`)

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/sololeveling.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## 🧪 Testing

### Run All Tests

```bash
# Auth flow test
python test/auth_flow_test.py

# Quest creation test
python test/test_quest_creation.py
```

### Test Coverage

- ✅ Registration (PASS)
- ✅ Login/Logout (PASS)
- ✅ Profile management (PASS)
- ✅ Quest creation (PASS)
- ✅ Learn & Explore routes (PASS)

---

## 🐛 Known Issues

### Minor
- [ ] Sound effects hook exists but audio files are missing (placeholder in static/sounds/)
- [ ] Tasks page uses legacy Bootstrap styling (migration to Tailwind pending)
- [ ] Logout button size may conflict with modal close button (UI refinement pending)

### Roadmap
- [ ] Quest analytics and statistics
- [ ] Leaderboard system
- [ ] Achievement shop (spend XP)
- [ ] Social/multiplayer quests
- [ ] PostgreSQL migration (production)
- [ ] Mobile app (React Native)

---

## 📚 Project Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System design, data models, API details
- **[PROJECT_PLAN.md](docs/PROJECT_PLAN.md)** — Status, roadmap, known issues
- **[PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)** — High-level summary and metrics
- **[CHANGELOG.md](CHANGELOG.md)** — Version history and changes
- **[QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** — Command cheatsheet

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Rami-Mhana**

- GitHub: [@Rami-Mhana](https://github.com/Rami-Mhana)
- Project: [Solo-Leveling-Personal-Development](https://github.com/Rami-Mhana/Solo-Leveling-Personal-Development)

---

## 🎯 Inspiration

Inspired by the *Solo Leveling* anime and the gamification of personal development. This project combines the immersive world-building of Solo Leveling with evidence-based personal development practices.

---

## 📞 Support

For issues, questions, or suggestions:
1. Check [PROJECT_PLAN.md](docs/PROJECT_PLAN.md) for known issues
2. Review [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) for troubleshooting
3. Open an issue on GitHub

---

**Last Updated**: December 3, 2025  
**Version**: 0.6.0-dev (Learn & Explore Update)
