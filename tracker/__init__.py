from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '850b0126f8f89a2637d77e2d29086569'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'johanna14'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_DB'] = 'tracker'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
UPLOAD_FOLDER = '/Users/ibafumba/PycharmProjects/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mbolokwa@gmail.com'  # todo put in environment variable?
app.config['MAIL_PASSWORD'] = 'johanna@14'  # todo put in environment variable?

mail = Mail(app)

from tracker.users.routes import users
from tracker.projects.routes import projects
from tracker.main.routes import main
from tracker.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(projects)
app.register_blueprint(main)
app.register_blueprint(errors)
