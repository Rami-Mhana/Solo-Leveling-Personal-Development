# Solo Leveling Personal Development - Architecture

## Project Overview

A gamified personal development Flask web application inspired by the Solo Leveling anime. Users complete quests, build habits, and progress through a leveling system with achievements.

**Stack**: Flask, SQLAlchemy, Jinja2, Tailwind CSS, Alpine.js

---

## System Architecture

### 1. Application Layers

```
┌─────────────────────────────────────┐
│      Frontend (Browser)             │
│  - Tailwind CSS (Dark Theme)        │
│  - Alpine.js (Interactions)         │
│  - Vanilla JS (Notifications)       │
└──────────────┬──────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────┐
│      Flask Routes & Views           │
│  - main_routes.py (Auth, Dashboard) │
│  - routes.py (Activity Endpoints)   │
│  - pd_routes.py (PD Features)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Business Logic                 │
│  - helpers.py (Activity Processing) │
│  - models.py (Data & Methods)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Data Layer                     │
│  - SQLAlchemy ORM                   │
│  - SQLite Database                  │
└─────────────────────────────────────┘
```

### 2. Data Models

#### User
- Core identity & authentication
- Character stats (Strength, Intelligence, Agility, Willpower, Discipline)
- Progression (XP, Level, Rank)
- Activity tracking (meditation, books, habits, goals, quests)
- Relationships:
  - `quests` → Quest (1:N)
  - `habits` → Habit (1:N)
  - `earned_achievements` → EarnedAchievement (1:N)

#### Quest
- User-created tasks/goals
- Difficulty ranking (E-S rank)
- XP rewards
- Completion status
- Deadline tracking

#### Achievement
- Achievement definitions (static)
- Categories: Fitness, Reading, Meditation, Social, Crafting
- Unlock conditions
- XP bonuses

#### EarnedAchievement
- User achievement unlocks (many:many with User)
- Timestamp tracking
- Maps `user_id` + `achievement_id` → earned_at

#### Habit
- Recurring activities
- Streak tracking (current & best)
- Frequency (daily, weekly, monthly)
- Completion history

---

## Feature Flows

### 1. Authentication Flow
```
User Registration
  → validate form (username, email, password)
  → check duplicates
  → hash password
  → create User record
  → auto-login
  → redirect to dashboard

User Login
  → validate credentials
  → check password hash
  → set session cookie
  → redirect to dashboard
```

### 2. Quest Completion Flow
```
User clicks "Complete" on quest
  → POST /complete-task { id }
  → Validate quest ownership
  → Mark quest completed
  → Award XP (quest.xp_reward)
  → Check level-up threshold
  → Update rank if leveled
  → Check achievements
  → Return JSON:
    {
      success: bool,
      notifications: [
        { type: 'levelup', message: '...', level, rank },
        { type: 'achievement', message: '...', achievement_id }
      ],
      progress: {
        level, rank, xp, xp_progress,
        stats: { strength, intelligence, ... },
        achievements: [{ id, earned_at }, ...]
      }
    }
  → Frontend:
    - Parse notifications
    - Play sounds
    - Update UI elements (data-* attributes)
    - Show animations
```

### 3. Stat Progression
```
Any activity completion:
  → update_stats() increments stat counter
  → check_achievements() evaluates conditions
  → EarnedAchievement records created
  → Frontend receives progress update
  → UI reflects new values
```

### 4. XP & Level System
```
LEVEL_THRESHOLDS:
  Level 1: 0 XP
  Level 2: 1000 XP
  Level 3: 2500 XP
  ...
  Level 10: 38000 XP

HUNTER_RANKS:
  Levels 1-2: E-Rank Hunter
  Levels 3-4: D-Rank Hunter
  Levels 5-6: C-Rank Hunter
  Levels 7-8: B-Rank Hunter
  Levels 9: A-Rank Hunter
  Level 10: S-Rank Hunter

XP_REWARDS:
  COMPLETE_QUEST: 100 XP
  MEDITATION_DAILY: 50 XP
  READ_BOOK: 150 XP
  COMPLETE_HABIT: 30 XP
  ACHIEVE_GOAL: 200 XP
```

---

## API Endpoints

### Authentication
- `POST /register` — Create new user account
- `POST /login` — Authenticate user
- `GET /logout` — End session

### Dashboard & Profile
- `GET /` — Main dashboard (requires auth)
- `GET /profile` — View/edit profile (requires auth)
- `POST /profile` — Update profile info

### Activities (Require Auth)
- `POST /complete-task` — Mark quest complete, award XP
- `POST /update-meditation` — Log meditation session
- `POST /complete-book` — Mark book as read
- `POST /complete-habit` — Log habit completion
- `POST /achieve-goal` — Mark goal achieved

### API Data
- `GET /api/progress` — Current user progress JSON
- `GET /api/achievements` — User's earned achievements

---

## Frontend Architecture

### Templates
Located in `app/templates/`:

1. **base.html** — Main layout
   - Responsive sidebar
   - Navigation
   - Notification queue
   - Achievement/Level-up display
   - Sound effect hooks

2. **dashboard.html** — User dashboard
   - XP bar & level display
   - Character stats bars
   - Active quests list
   - Quest completion buttons

3. **profile.html** — User profile
   - User info & avatar
   - Edit form
   - Detailed stats
   - Rank display

4. **login.html** — Authentication
5. **register.html** — User signup
6. **tasks.html** — Quest management
7. **pd_profile.html** — Personal development profile

### JavaScript
**achievements.js** — Client-side achievement system
- Achievement definitions
- XP reward mapping
- Level thresholds & ranks
- `checkAchievements(stats)` — Evaluate unlock conditions
- `checkLevelUp(xp, level)` — Detect level progression
- Event listeners for animations

**base.html inline**:
- `notificationSystem` — Manage notification queue
- `completeActivity(type, id)` — Unified activity endpoint handler
- DOM update logic for stats/progress
- Sound effect playback

### CSS
**style.css** — Custom styling:
- Gaming color scheme
- Neon effects
- Animations (slide-in, fade, particles)
- Responsive layout

**Tailwind CDN** — Utility classes
- Layout
- Typography
- Spacing
- Colors

### Data Attributes (Frontend Targeting)
```html
data-user-level          <!-- Level display -->
data-user-rank           <!-- Rank display -->
data-user-name           <!-- Username display -->
data-xp-bar              <!-- XP progress bar (width %) -->
data-xp-text             <!-- XP text (current/max) -->
data-stat="strength"     <!-- Stat bar (width %) -->
data-activity="123"      <!-- Quest/activity container -->
data-activity-id="123"   <!-- Activity identifier -->
```

---

## Database Schema

### Tables
1. **user** — User accounts & progression
2. **quest** — User-created quests
3. **habit** — Recurring habits
4. **achievement** — Achievement definitions
5. **earned_achievement** — User achievement unlocks

### Relationships
```
User (1) ──→ (N) Quest
User (1) ──→ (N) Habit
User (1) ──→ (N) EarnedAchievement ←── Achievement
```

---

## Request/Response Cycle

### POST /complete-task

**Request**:
```json
{
  "id": "123",
  "type": "task"
}
```

**Processing**:
1. Load quest by ID
2. Verify user ownership
3. Update quest.completed = True
4. Calculate XP: User.xp += quest.xp_reward
5. Check level thresholds
6. Update rank if needed
7. Check achievements
8. Commit transaction
9. Build progress object

**Response**:
```json
{
  "success": true,
  "message": "Quest completed!",
  "xp_gained": 100,
  "notifications": [
    {
      "type": "levelup",
      "message": "Advanced to Level 2!",
      "details": { "level": 2, "rank": "E-Rank Hunter" }
    }
  ],
  "progress": {
    "level": 2,
    "rank": "E-Rank Hunter",
    "xp": 100,
    "xp_progress": 10.0,
    "stats": {
      "strength": 10,
      "intelligence": 10,
      ...
    },
    "achievements": [...]
  }
}
```

**Frontend**:
1. Parse response
2. Show notifications (achievements, level-ups)
3. Play sounds
4. Update DOM (data-* elements)
5. Animate progress bars
6. Remove completed quest from list

---

## File Structure

```
app/
├── __init__.py          → Application factory
├── models.py            → SQLAlchemy models
├── helpers.py           → Business logic (process_activity, update_stats)
├── routes.py            → Activity endpoints + API
├── main_routes.py       → Auth + dashboard routes
├── pd_routes.py         → Personal dev routes
├── static/
│   ├── css/style.css    → Custom styling
│   ├── js/achievements.js → Achievement system
│   └── sounds/          → Audio assets (placeholder)
└── templates/
    ├── base.html        → Main layout
    ├── dashboard.html   → User dashboard
    ├── profile.html     → User profile
    ├── login.html       → Login form
    ├── register.html    → Registration form
    ├── tasks.html       → Quest management
    └── pd_profile.html  → PD profile view

config.py               → Flask configuration
create_db.py           → Database initialization
run.py                 → Development server
wsgi.py                → Production entry point

test/
├── auth_flow_test.py  → Register/login/profile tests
├── debug_register.py  → Registration debugging
└── import_app_debug.py → Import validation
```

---

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.1.2 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM wrapper |
| Flask-Login | 0.6.3 | Session management |
| SQLAlchemy | 2.0.43 | ORM |
| Werkzeug | 3.1.3 | WSGI utilities |
| Jinja2 | 3.1.6 | Template engine |

---

## Transaction Management

### Current State
- Commits happen within model methods (`add_xp()`)
- Helper functions commit after updates

### Recommended Improvement
- Move commits to route level
- Use transaction context managers
- Consolidate multiple DB writes per request

```python
# Future pattern
@app.route('/complete-task', methods=['POST'])
def complete_task():
    with db.session.begin_nested():
        quest.completed = True
        user.xp += quest.xp_reward
        user._update_rank()
        new_achievements = user.check_achievements()
    # Single commit after context exits
    db.session.commit()
    return jsonify(...)
```

---

## Deployment Notes

### Development
```bash
python run.py
# Runs on http://127.0.0.1:5000
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Database
- Development: SQLite (`instance/sololeveling.db`)
- Environment-based via `SQLALCHEMY_DATABASE_URI`

---

## Known Limitations & Future Work

1. **Database**
   - No migrations framework (Alembic) — manual schema updates needed
   - SQLite — not suitable for production load

2. **Authentication**
   - No password reset flow
   - No email verification
   - No OAuth integration

3. **Features**
   - Single-player only (no multiplayer)
   - No reward shop
   - Limited achievement conditions

4. **Performance**
   - No query caching
   - N+1 query risks
   - No pagination for quests

5. **UI/UX**
   - Sound files missing (placeholder hooks exist)
   - Limited mobile optimization
   - No dark mode toggle

6. **Testing**
   - Auth tests only
   - No achievement/XP system tests
   - No integration tests

---

## Next Steps (Roadmap)

### Phase 1: Stability ✅ (In Progress)
- [x] Fix register route bug
- [x] Validate auth flows
- [ ] Add sound assets
- [ ] Create DB migration

### Phase 2: Features
- [ ] Achievement system tests
- [ ] Reward shop
- [ ] Leaderboard
- [ ] Social features

### Phase 3: Quality
- [ ] Consolidate transactions
- [ ] Add caching
- [ ] Improve error handling
- [ ] Full test coverage

### Phase 4: Deployment
- [ ] Alembic migrations
- [ ] Environment config
- [ ] Production setup
- [ ] Monitoring & logging
