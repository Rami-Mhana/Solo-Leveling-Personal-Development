# Changelog

All notable changes to the Solo Leveling Personal Development project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] — Dec 3, 2025

### Added

#### New Features
- **Learn & Explore** (`/learn`) — New section with quotes, learning approaches, patterns, and personal development rules
  - `learn_routes.py` — Learning blueprint with 4 sub-routes
  - `learn_explore.html` — Main learning dashboard with tabbed content
  - Added "Learn & Explore" link to sidebar navigation
  - 20+ pre-loaded quotes, 5 approaches, 4 patterns, 6 rules

- **Database Migration System** 
  - `migrate_db.py` — Standalone migration script for safe schema updates
  - Seeds 6 core achievement definitions automatically
  - Safe drop/create for dev environments

#### Refactoring & Improvements
- **Stats Architecture Refactored**
  - User model now uses JSON-based `core_stats` (system-defined) and `player_stats` (user-defined)
  - Backward-compatible properties for existing code
  - Cleaner separation of concerns (fixed vs. user-defined metrics)
  
- **Achievement System Fixed**
  - Removed erroneous `user_id` FK from `Achievement` model (now global definitions)
  - `EarnedAchievement.achievement_id` changed from String to Integer FK
  - Added proper relationship to `Achievement` model
  - Updated `check_achievements()` to use Achievement titles for lookup
  - All 6 achievements now properly tracked in database

- **Data Model Integrity**
  - Added `achievement` relationship to `EarnedAchievement`
  - Fixed foreign key constraints
  - Improved migration resilience

### Fixed

- ✅ Achievement model FK corruption (removed user_id)
- ✅ EarnedAchievement type mismatch (String → Integer achievement_id)
- ✅ Stats storage inconsistency (single columns → JSON structure)
- ✅ Database initialization now includes achievement seed data
- ✅ Auth flow tests updated for in-memory DB isolation

### Changed

- Stats are now stored as JSON objects for better flexibility
- Achievement definitions are now globally maintained in the database
- Models use properties for backward compatibility with templates
- Migration handled via `migrate_db.py` (run once per environment)

### Technical Debt Addressed

- ✅ Data model now reflects true domain model (global achievements, per-user earnings)
- ✅ Cleaner separation between system-defined and user-defined stats
- ✅ Better FK integrity with proper relationships

---

## [v0.5.0-alpha] — Previous Release

### Added
- Core gamification system (XP, levels, ranks)
- Authentication (register, login, logout)
- Quest/task management
- Achievement tracking
- User profile with stats
- Dark gaming UI theme
- Notification system with animations
- Flask-based REST API

### Status: Working Core Features
- ✅ User auth (register/login/logout)
- ✅ Quest creation and completion
- ✅ XP and level progression
- ✅ Achievement unlock conditions
- ✅ Responsive dark theme UI

---

## Roadmap

### Near-term (This Month)
- [ ] UI Polish — Fix logout button spacing, migrate tasks.html to Tailwind
- [ ] Enhanced Testing — Add integration tests for quests, achievements
- [ ] Documentation — Update README with new features
- [ ] Sound Assets — Add achievement/levelup audio files

### Medium-term (Next Sprint)
- [ ] Quest Analytics — Track completion rates, time-to-complete
- [ ] Habit Streaks — Visual streak counter and rewards
- [ ] Leaderboards — Compare stats with other users
- [ ] Achievement Shop — Spend XP on cosmetics

### Long-term (Next Quarter)
- [ ] Social Features — Friend quests, multiplayer challenges
- [ ] PostgreSQL Migration — Production database support
- [ ] CI/CD Pipeline — Automated testing and deployment
- [ ] Mobile App — React Native companion

---

## Migration Guide

### If You're Updating from v0.4.x

1. **Back up your database**
   ```bash
   cp instance/sololeveling.db instance/sololeveling.db.backup
   ```

2. **Run the migration**
   ```bash
   python migrate_db.py
   ```
   This will:
   - Create new tables with fixed schema
   - Seed achievement definitions
   - Preserve your user data

3. **Test locally**
   ```bash
   python test/auth_flow_test.py
   python test/test_quest_creation.py
   ```

---

## Contributors

- **Rami-Mhana** — Lead development

---

*Last updated: December 3, 2025*
