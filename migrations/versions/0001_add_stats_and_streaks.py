"""add system/player stat columns and streak fields

Revision ID: 0001_add_stats_and_streaks
Revises: 
Create Date: 2025-12-06
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_add_stats_and_streaks'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add system-defined stat columns with sensible defaults for existing rows
    op.add_column('user', sa.Column('system_strength', sa.Integer(), nullable=False, server_default='10'))
    op.add_column('user', sa.Column('system_intelligence', sa.Integer(), nullable=False, server_default='10'))
    op.add_column('user', sa.Column('system_agility', sa.Integer(), nullable=False, server_default='10'))
    op.add_column('user', sa.Column('system_willpower', sa.Integer(), nullable=False, server_default='10'))
    op.add_column('user', sa.Column('system_discipline', sa.Integer(), nullable=False, server_default='10'))

    # Add player-defined name/value pairs (5 slots)
    op.add_column('user', sa.Column('player_stat_1_name', sa.String(length=100), nullable=False, server_default='stat1'))
    op.add_column('user', sa.Column('player_stat_1_value', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user', sa.Column('player_stat_2_name', sa.String(length=100), nullable=False, server_default='stat2'))
    op.add_column('user', sa.Column('player_stat_2_value', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user', sa.Column('player_stat_3_name', sa.String(length=100), nullable=False, server_default='stat3'))
    op.add_column('user', sa.Column('player_stat_3_value', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user', sa.Column('player_stat_4_name', sa.String(length=100), nullable=False, server_default='stat4'))
    op.add_column('user', sa.Column('player_stat_4_value', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user', sa.Column('player_stat_5_name', sa.String(length=100), nullable=False, server_default='stat5'))
    op.add_column('user', sa.Column('player_stat_5_value', sa.Integer(), nullable=False, server_default='0'))

    # Add streak fields
    op.add_column('user', sa.Column('last_login_date', sa.Date(), nullable=True))
    op.add_column('user', sa.Column('streak_count', sa.Integer(), nullable=False, server_default='0'))

    # Remove server defaults for cleanliness (optional)
    with op.get_context().autocommit_block():
        for col in ['system_strength','system_intelligence','system_agility','system_willpower','system_discipline',
                    'player_stat_1_value','player_stat_2_value','player_stat_3_value','player_stat_4_value','player_stat_5_value','streak_count']:
            op.alter_column('user', col, server_default=None)


def downgrade():
    # Drop streak fields
    op.drop_column('user', 'streak_count')
    op.drop_column('user', 'last_login_date')

    # Drop player stat columns
    op.drop_column('user', 'player_stat_5_value')
    op.drop_column('user', 'player_stat_5_name')
    op.drop_column('user', 'player_stat_4_value')
    op.drop_column('user', 'player_stat_4_name')
    op.drop_column('user', 'player_stat_3_value')
    op.drop_column('user', 'player_stat_3_name')
    op.drop_column('user', 'player_stat_2_value')
    op.drop_column('user', 'player_stat_2_name')
    op.drop_column('user', 'player_stat_1_value')
    op.drop_column('user', 'player_stat_1_name')

    # Drop system stat columns
    op.drop_column('user', 'system_discipline')
    op.drop_column('user', 'system_willpower')
    op.drop_column('user', 'system_agility')
    op.drop_column('user', 'system_intelligence')
    op.drop_column('user', 'system_strength')
