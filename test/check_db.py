from app.market import create_app, db
from app.market.models import Item

app = create_app()
with app.app_context():
    print("Connected to:", db.engine.url.database)
    print("Tables:", db.inspect(db.engine).get_table_names())


    