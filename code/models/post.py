from db import db
from datetime import datetime
from models.comments import CommentsModel
from models.like import LikeModel

class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    total_likes = db.Column(db.Integer, default=0)
    total_dislikes = db.Column(db.Integer, default=0)
    last_modified = db.Column(db.DateTime, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('CommentsModel', backref='post', cascade='all,delete')
    like_obj = db.relationship('LikeModel', backref='post', cascade='all,delete')


    def __init__(self, content, author_id):
        self.content = content
        self.author_id = author_id
        self.last_modified = datetime.now()

    def json(self):
        from models.user import UserModel
        try:
            user = UserModel.find_by_id(self.author_id)
        except NoResultFound as e:
            return {'message':'user does not exist !'}, 400
        return {'author': user.username , 'content':self.content, 'Total Likes': self.total_likes}

    @classmethod
    def find_by_id(cls, id):
        post = PostModel.query.filter_by(id = id).first()
        return post

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
