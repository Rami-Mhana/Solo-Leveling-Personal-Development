from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    db.create_all()
    users = User.query.all()
    print('User count:', len(users))
    for u in users:
        print(u.id, u.username, u.email)
