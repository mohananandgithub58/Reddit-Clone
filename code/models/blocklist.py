from db import db
from sqlalchemy.exc import (
    NoResultFound,
    CompileError,
    InternalError,
    DisconnectionError,
    IdentifierError,
    TimeoutError
)
from datetime import datetime

class TokenBlockListModel(db.Model):
    __tablename__ = 'tokenblocklist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logged_in_at = db.Column(db.DateTime, nullable=False)
    logged_out_at = db.Column(db.DateTime)
    revoked_status = db.Column(db.Integer, default=0, nullable=False)
    fresh_jti = db.Column(db.String(30), nullable=False, unique=True)
    refresh_jti = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, user_id, fresh_jti, refresh_jti):
        self.user_id = user_id
        self.fresh_jti = fresh_jti
        self.refresh_jti = refresh_jti
        self.logged_in_at = datetime.now()

    def update_block_list(self, fresh_jti, refresh_jti):
        self.fresh_jti = fresh_jti
        self.refresh_jti = refresh_jti
        self.logged_in_at = datetime.now()
        self.logged_out_at = None
        self.revoked_status = 0
        db.session.commit()

    def add_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
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

    def delete_from_db(self):
        try:
            db.session.delete()
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

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(user_id = userid).first()

    @classmethod
    def find_by_jti(cls, jti):
        try:
            token = cls.query.filter((TokenBlockListModel.fresh_jti == jti) | (TokenBlockListModel.refresh_jti == jti)).first()
        except NoResultFound:
            return None
        else:
            return token

    def get_revoked_status(self):
        return self.revoked_status

    def set_jti(self, jti):
        self.refresh_jti = jti
        self.logged_in_at = datetime.now()
        db.session.commit()

    def logout(self):
        self.revoked_status = 1
        self.logged_out_at = datetime.now()
        db.session.commit()
