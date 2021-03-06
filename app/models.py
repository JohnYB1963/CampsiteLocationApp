from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


favorites = db.Table('favorites',
    db.Column('campsite_id', db.Integer, db.ForeignKey('campsite.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(24))
    last_name = db.Column(db.String(24))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    favorites = db.relationship('Campsite', secondary=favorites, lazy='subquery')
    reviews = db.relationship('Review', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size=160):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Campsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.String(20))
    park_id = db.Column(db.String(20))
    facility_name = db.Column(db.String(60))
    description = db.Column(db.Text)
    img = db.Column(db.String())

    def __repr__(self):
        return '<{}:{}>'.format(self.contract_id, self.park_id)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contract_id = db.Column(db.String(20))
    park_id = db.Column(db.String(20))
