"""Quick DB smoke test.

This uses the central app factory and the DB instance defined in `app.models`.
"""

from app import create_app
from app.models import db
from app.market.models import Item


def main():
    app = create_app()
    with app.app_context():
        try:
            print('Connected to:', db.engine.url)
            inspector = db.inspect(db.engine)
            print('Tables:', inspector.get_table_names())
        except Exception as e:
            print('DB check failed:', e)


if __name__ == '__main__':
    main()


    