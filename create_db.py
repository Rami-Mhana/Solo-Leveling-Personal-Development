# create_db.py (project root)
from app.market import create_app, db  # adjust import if create_app lives elsewhere
# What is create_app ?
import os # OS Module(Not a class, it's a fucken whole file I think!)

app = create_app()

with app.app_context():
    # import your models so SQLAlchemy knows about them
    # e.g. from app.market import models   OR  from app import models
    # replace the line below with the correct import for your project
    try:
        from app.market import models
    except Exception:
        pass
    # Does this mean that in all cases create the .db file(database)? Because will have an exception but we will pass!
    db.create_all()
    print("database created (sqlite file should appear in your project folder)")

    """
    Or I should put this:
    
    with app.app_context():
    # import your models so SQLAlchemy knows about them
    # e.g. from app.market import models   OR  from app import models
    # replace the line below with the correct import for your project
    try:
        from app.market import models
        db.create_all()
        print("database created (sqlite file should appear in your project folder)")

    except Exception:
        print("Not working")
        pass

    """

    print("SQLALCHEMY_DATABASE_URI =", app.config.get("SQLALCHEMY_DATABASE_URI"))
    print("current working dir (cwd)   =", os.getcwd())
    print("Flask instance_path         =", app.instance_path)
    db.create_all()
    print("done — DB created where above URI indicates")


    