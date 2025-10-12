import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'market.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret'
    # Add database URI later, e.g., SQLALCHEMY_DATABASE_URI = 'mysql://user:password@host/db_name'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    # What is this?
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # Email server settings
    # MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


# Example usage: