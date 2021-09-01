from db import db
from datetime import datetime


class CommentsModel(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    commented_at = db.Column(db.DateTime, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user_id, post_id, content):
        self.content = content
        self.post_id = post_id
        self.user_id = user_id
        self.commented_at = datetime.now()

    def json(self):
        from models.user import UserModel
        user = UserModel.find_by_id(self.user_id)
        return {f'post id ' : self.post_id, 'user ' : user.username, 'content ' : self.content}

    def save_to_db(self):
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
