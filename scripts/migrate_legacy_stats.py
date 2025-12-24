#!/usr/bin/env python3
"""
Idempotent data migration script to copy legacy JSON stats into explicit columns.

Usage (from project root, with venv activated if needed):

$env:PYTHONPATH='.'; python .\scripts\migrate_legacy_stats.py

This script will:
- Read `core_stats` JSON and map keys to `system_strength`, `system_intelligence`,
  `system_agility`, `system_willpower`, `system_discipline` when those columns
  are currently NULL.
- Read `player_stats` JSON (dict or list form) and populate the first available
  `player_stat_N_name` / `player_stat_N_value` slots when empty, or fill
  missing values for matching stat names.

The operation is non-destructive and idempotent: it will not overwrite
non-null explicit columns.
"""
import json
import sys
from typing import Any

from app import create_app, db
from app.models import User


def parse_json_field(value: Any):
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return None
    return None


def migrate_user(u: User) -> bool:
    """Return True if user was modified."""
    changed = False

    core = parse_json_field(getattr(u, 'core_stats', None))
    mapping = {
        'strength': 'system_strength',
        'intelligence': 'system_intelligence',
        'agility': 'system_agility',
        'willpower': 'system_willpower',
        'discipline': 'system_discipline',
    }

    if isinstance(core, dict):
        for k, target in mapping.items():
            # try multiple key casings for robustness
            val = core.get(k)
            if val is None:
                val = core.get(k.capitalize())
            if val is None:
                val = core.get(k.title())

            cur = getattr(u, target, None)
            # only set when current value is None
            if cur is None and val is not None:
                try:
                    setattr(u, target, int(val))
                    changed = True
                except Exception:
                    # ignore bad cast
                    pass

    # player_stats may be a dict {name: value} or a list [{name:..., value:...}]
    pstats = parse_json_field(getattr(u, 'player_stats', None))
    items = []
    if isinstance(pstats, dict):
        items = list(pstats.items())
    elif isinstance(pstats, list):
        for el in pstats:
            if isinstance(el, dict):
                # try common shapes
                name = el.get('name') or el.get('stat')
                val = el.get('value') or el.get('val') or el.get('amount')
                if name is None and len(el) == 1:
                    # e.g. [{"Strength": 5}]
                    k = next(iter(el.keys()))
                    name = k
                    val = el[k]
                if name is not None:
                    items.append((str(name), val))

    # populate player_stat_N_name/value slots
    for i in range(1, 6):
        name_attr = f'player_stat_{i}_name'
        val_attr = f'player_stat_{i}_value'
        cur_name = getattr(u, name_attr, None)
        cur_val = getattr(u, val_attr, None)

        # If name exists and value is missing, try to find in items by name
        if cur_name and (cur_val is None):
            for idx, (n, v) in enumerate(items):
                if isinstance(n, str) and n.strip().lower() == str(cur_name).strip().lower():
                    if v is not None:
                        try:
                            setattr(u, val_attr, int(v))
                            changed = True
                        except Exception:
                            pass
                    # remove matched item
                    items.pop(idx)
                    break

        # If name slot empty, fill from next remaining item
        if not cur_name and items:
            n, v = items.pop(0)
            try:
                setattr(u, name_attr, str(n))
                setattr(u, val_attr, int(v) if v is not None else 0)
                changed = True
            except Exception:
                pass

    return changed


def main():
    app = create_app()
    with app.app_context():
        users = User.query.order_by(User.id).all()
        total = len(users)
        print(f'Found {total} users to inspect')

        updated = 0
        updated_ids = []
        for u in users:
            try:
                if migrate_user(u):
                    updated += 1
                    updated_ids.append(u.id)
                    db.session.add(u)
            except Exception as e:
                print(f'Error processing user id={u.id}:', e)

        if updated:
            db.session.commit()

        print(f'Updated {updated} users: {updated_ids}')


if __name__ == '__main__':
    main()
