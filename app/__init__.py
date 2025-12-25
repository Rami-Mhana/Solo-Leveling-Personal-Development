import os
from flask import Flask
from flask_login import LoginManager
from .models import db, User  # Import User model for Flask-Login
from config import Config  # Import Config from the root level


def create_app(test_config=None):
    """Application factory.

    Creates the Flask app, configures SQLAlchemy, and registers blueprints.
    """
    # Explicit template/static folder paths (ensure Jinja finds app/templates)
    pkg_dir = os.path.dirname(__file__)
    templates_path = os.path.join(pkg_dir, 'templates')
    static_path = os.path.join(pkg_dir, 'static')

    app = Flask(__name__, instance_relative_config=True, template_folder=templates_path, static_folder=static_path)
    
    # Load configuration from Config class
    app.config.from_object(Config)

    # Configure app from mapping (overrides Config and sets instance path correctly for dev)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Use Flask's instance_path for the DB file location
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'sololeveling.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register application blueprints (routes)
    from .main_routes import main_bp
    app.register_blueprint(main_bp)

    # Register personal development blueprint
    from .pd_routes import pd_bp
    app.register_blueprint(pd_bp, url_prefix='/pd')

    # Register learning blueprint
    from .learn_routes import learn_bp
    app.register_blueprint(learn_bp, url_prefix='/learn')

    # Register the legacy blueprint (renamed app.py to legacy_routes.py)
    try:
        from .legacy_routes import legacy_bp
        # Use url_prefix to namespace the demo routes
        app.register_blueprint(legacy_bp, url_prefix='/legacy')
    except ImportError:
        pass

    return app