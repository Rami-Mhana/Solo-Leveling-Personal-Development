from sqlalchemy import create_engine, inspect, text
from app import create_app

app = create_app()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
ins = inspect(engine)
print('Tables:', ins.get_table_names())
if 'user' in ins.get_table_names():
    cols = ins.get_columns('user')
    print('\nUser table columns:')
    for c in cols:
        print(' -', c['name'], c['type'], 'nullable=', c.get('nullable'), 'default=', c.get('default'))
    # show a sample row
    with engine.connect() as conn:
        try:
            stmt = text('SELECT id, username, xp, level, system_strength, player_stat_1_value, last_login_date, streak_count FROM user LIMIT 5')
            r = conn.execute(stmt).fetchall()
            print('\nSample rows:')
            for row in r:
                print(row)
        except Exception as e:
            print('Error reading sample rows:', e)
