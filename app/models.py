from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(255))

    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'


class Pitch(db.Model):
    __tablename__ = 'goal_pitch'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    comments = db.relationship(
        'Comment', backref="main_pitch", cascade="all, delete-orphan", lazy="dynamic")

    def __repr__(self):
        return f'User {self.title}'


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    pitch = db.relationship('Pitch', backref='parent_category', lazy='dynamic')

    def __repr__(self):
        return f'Category {self.name}'


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255))
    comment = db.Column(db.String)

    goal_pitch_id = db.Column(db.Integer, db.ForeignKey("goal_pitch.id"))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
