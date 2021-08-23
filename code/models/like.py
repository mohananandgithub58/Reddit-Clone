from db import db

class LikeModel(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, status, post_id, user_id):
        self.status = status
        self.post_id = post_id
        self.user_id = user_id

    def get_like_status(self):
        return status

    def find_by_id(post_id):
        like = LikeModel.query.filter_by(post_id).first()
        return like


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
