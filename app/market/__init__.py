import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__) # Create an instance of Flask class | __name__ is a special variable in Python that represents the name of the current module.
    # Configure the SQLite database, relative to the app instance folder
    
    # Make absolute path to ensure one single .db file is used everywhere
    basedir = os.path.abspath(os.path.dirname(__file__)) # What is __file__? | It is a special variable in Python that represents the path to the current file.
    db_path = os.path.join(basedir, '..', 'instance', 'market.db') # What is .. ? | It means parent directory. Which is the instance folder in this case. 
    # The join() method joins one or more path components intelligently. and it's parameters are: (base directory, parent directory, database file name)
    
    # Ensure the instance folder exists
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app) # What is init_app()? | It is a method that binds the database instance to the Flask app instance.
    
    with app.app_context(): # What is app_context()? | It is a method that creates an application context.
        from . import models
        db.create_all()  # ensures tables exist before first query

    return app


    