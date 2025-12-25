# Model & Routing Updates

This file documents the recent backend and data-model updates made during the
`refactor/ui-ux-and-database` work.

Key changes

- System-defined core stats (explicit columns) were added/renamed to clarify
  they are managed by the system:
  - `system_strength` (Integer)
  - `system_intelligence` (Integer)
  - `system_agility` (Integer)
  - `system_willpower` (Integer)
  - `system_discipline` (Integer)

- Player-defined stats: five name/value pairs were added so users can track
  arbitrary metrics. Each pair contains a `name` (String) and a `value` (Integer):
  - `player_stat_1_name`, `player_stat_1_value`
  - ... up to `player_stat_5_name`, `player_stat_5_value`

- Streak tracking fields were added to the `User` model:
  - `last_login_date` (Date)
  - `streak_count` (Integer, default 0)

Routing / Behavior

- The login flow now updates `last_login_date` and `streak_count` upon successful
  authentication. Behaviour:
  - If `last_login_date` is `None`, streak becomes 1.
  - If `last_login_date` == yesterday, increment `streak_count` by 1.
  - If `last_login_date` < yesterday, reset `streak_count` to 1.
  - If `last_login_date` == today, do nothing.
  - `last_login_date` is saved as today's date after processing.

- A top-level endpoint alias `home` was added so `url_for('home')` resolves to the
  main index view (same as `main.index`).

Database / Migrations

- Alembic migration scripts were scaffolded and a migration to add the above
  columns exists under `migrations/versions/`. If you need to apply the
  migration locally run:

```powershell
alembic upgrade head
```

Data migration helper

- An idempotent helper script was added at `scripts/migrate_legacy_stats.py` to
  copy values from legacy `core_stats` / `player_stats` JSON fields into the new
  explicit columns when those columns are empty. The script is safe to re-run.

If you need any of these behaviours adjusted (for example treating zeros as
empty and overwriting them), open an issue or ask for a follow-up patch.

---
Generated on 2025-12-06
