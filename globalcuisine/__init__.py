from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click

# Initialize the database
db = SQLAlchemy()

# Application Factory
def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///globalcuisine.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'globalcuisine/static/images'

    db.init_app(app)

    migrate = Migrate(app, db)
    
    @app.cli.command('create-admin')
    @with_appcontext
    def create_admin():
        from models import User  # Importing here to avoid circular imports
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('securepassword')  # Assuming you have a set_password method to hash the password
            db.session.add(admin)
            db.session.commit()
            click.echo('Admin user created.')
        else:
            click.echo('Admin user already exists.')

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # User loader function for Flask-Login
    from .models import User
    with app.app_context():
        db.drop_all()
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Import the main Blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
