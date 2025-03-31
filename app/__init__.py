from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

@login_manager.user_loader
def load_user(id):
    from app.models import User
    return User.query.get(int(id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Set up login configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes import auth, main, portfolio, dashboard, config
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(portfolio.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(config.bp)

    return app

# Import models to ensure they are registered with SQLAlchemy
from app.models import User, PortfolioItem 