import os

# The base directory where config.py is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret'
    # SQLALCHEMY_DATABASE_URI is dynamically set in app/__init__.py to point to the instance folder for better structure.
    # This is kept as a fallback or standard configuration object.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'sololeveling.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Why this false? To disable a Flask-SQLAlchemy feature that signals the app every time a change is about to be made in the database. This is unnecessary overhead and can be turned off. What does it do? It helps to reduce memory usage and improve performance.