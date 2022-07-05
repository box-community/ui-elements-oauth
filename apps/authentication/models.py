# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
import hashlib
from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Access_Token(db.Model):
    __tablename__ = 'access_token'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # user = db.relationship('Users', backref=db.backref('access_token', lazy=True))

    def __repr__(self):
        return '<Access_Token %r>' % self.access_token

class Csrf_token(db.Model):
    __tablename__ = 'Csrf_token'
    token = db.Column(db.String(100), primary_key=True)
    
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return str(self.token)

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    avatar_url = db.Column(db.String(512))

    def __init__(self, **kwargs):
        email = kwargs.get('email')
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            if property == 'avatar_url':
                if value is None:
                    value = 'https://www.gravatar.com/avatar/'+hashlib.md5(email.lower().encode('utf-8')).hexdigest()+'?d=identicon'

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('email')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     user = Users.query.filter_by(username=username).first()
#     return user if user else None