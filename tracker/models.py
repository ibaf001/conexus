import json
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tracker import db, login_manager, app
from flask_login import UserMixin


class Employee:
    def __init__(self, id, code, name):
        self.id = id
        self.name = name
        self.code = code





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # projects = db.relationship('Project', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     code = db.Column(db.String(10), unique=True, nullable=False)
#     date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     client = db.Column(db.String(10), nullable=False)
#     county = db.Column(db.String(10), nullable=False)
#     municipality = db.Column(db.String(10), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#     def __repr__(self):
#         return f"Project('{self.client}', '{self.code}')"


