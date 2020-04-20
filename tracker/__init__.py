from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from tracker.config import Config

# UPLOAD_FOLDER = '/Users/ibafumba/PycharmProjects/uploads'  todo need to remove this line
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # This is how we tell flask with config to use

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from tracker.users.routes import users
    from tracker.projects.routes import projects
    from tracker.main.routes import main
    from tracker.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(projects)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
