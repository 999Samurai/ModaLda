from flask_login import UserMixin

from login_manager import login_manager
from database import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    role = db.Column(db.String())
    last_login = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<User {self.id}>"
