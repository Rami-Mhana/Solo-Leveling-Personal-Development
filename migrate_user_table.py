"""
Migration script to add missing columns to user table.
Adds: last_active_date, streak_freeze_inventory
"""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path('instance/sololeveling.db')

def migrate_user_table():
    """Add missing columns to user table without dropping data."""
    
    if not DB_PATH.exists():
        print("ERROR: Database not found at instance/sololeveling.db")
        return False
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        print("Connecting to database...")
        print(f"Database: {DB_PATH}")
        print()
        
        # Check current columns
        cursor.execute("PRAGMA table_info(user)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        print("Existing columns in user table:")
        for col in sorted(existing_columns):
            print(f"  - {col}")
        print()
        
        # Add missing columns if they don't exist
        columns_to_add = [
            ('last_active_date', 'DATE'),
            ('streak_freeze_inventory', 'INTEGER DEFAULT 0'),
        ]
        
        for col_name, col_type in columns_to_add:
            if col_name not in existing_columns:
                sql = f"ALTER TABLE user ADD COLUMN {col_name} {col_type}"
                print(f"Adding column: {col_name} ({col_type})")
                cursor.execute(sql)
                print(f"  ✓ Column '{col_name}' added successfully")
            else:
                print(f"✓ Column '{col_name}' already exists, skipping")
        
        conn.commit()
        print()
        
        # Verify new schema
        cursor.execute("PRAGMA table_info(user)")
        updated_columns = [col[1] for col in cursor.fetchall()]
        print("Updated columns in user table:")
        for col in sorted(updated_columns):
            print(f"  ✓ {col}")
        
        conn.close()
        print()
        print("="*60)
        print("MIGRATION SUCCESSFUL!")
        print("="*60)
        print()
        print("Your database is now updated with the new columns.")
        print("You can now run: python run.py")
        print()
        
        return True
        
    except sqlite3.Error as e:
        print(f"ERROR: {e}")
        return False

if __name__ == '__main__':
    success = migrate_user_table()
    exit(0 if success else 1)
