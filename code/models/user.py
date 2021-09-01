from db import db
from datetime import datetime
import re
from sqlalchemy.exc import (
    IntegrityError,
    CompileError,
    DisconnectionError,
    IdentifierError,
    InternalError,
    TimeoutError,
    NoResultFound
)
from models.post import PostModel
from models.comments import CommentsModel
from models.like import LikeModel
from models.blocklist import TokenBlockListModel

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80))
    about = db.Column(db.String(80))
    creation_date = db.Column(db.DateTime, nullable=False)
    posts = db.relationship('PostModel', backref='author',  cascade='all,delete')
    comments = db.relationship('CommentsModel', backref='commenter', cascade='all,delete')
    like_status = db.relationship('LikeModel', backref='user', cascade='all,delete')
    login_logout_status = db.relationship('TokenBlockListModel', backref='login_status', cascade='all, delete')


    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.creation_date = datetime.now()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).one()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).one()

    @staticmethod
    def validate_password(password):
        flag = 0
        if len(password) > 7:
            flag += 1
        if re.search("[a-z]", password):
            flag += 1
        if re.search("[A-Z]", password):
            flag += 1
        if re.search("[0-9]", password):
            flag += 1
        if re.search("[_@!$%*]", password):
            flag += 1
        if flag == 5:
            return True
        else:
            return False

    def update_user_name(self, name):
        data = db.query.filter_by(id = id).first()
        return data

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message':'user already exists !'}, 400
        except CompileError or InternalError:
            db.session.rollback()
            return {'message':'an unknown error occured !'}, 500
        except DisconnectionError:
            db.sesson.rollback()
            return {'message':'Database disconnected !'}, 200
        except IdentifierError:
            db.session.rollback()
            return {'message':'character limit exceeded, kindly check !'}, 200
        except TimeoutError:
            db.session.rollback()
            return {'message':'session timed out !'}, 200
        else:
            return {'message':'user created !'}, 201

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except CompileError or InternalError:
            db.session.rollback()
            return {'message':'an unknown error occured !'}, 500
        except DisconnectionError:
            db.sesson.rollback()
            return {'message':'Database disconnected !'}, 200
        except TimeoutError:
            db.session.rollback()
            return {'message':'session timed out !'}, 200
