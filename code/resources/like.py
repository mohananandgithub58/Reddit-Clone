from flask_restful import Resource, reqparse
from models.like import LikeModel
from flask_jwt_extended import jwt_required
from models.post import PostModel
from models.user import UserModel
from sqlalchemy.exc import NoResultFound

class LikeAPost(Resource):
    @jwt_required()
    def post(self, username, post_id):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message':'user does not exist !'}, 400
        post = PostModel.find_by_id(post_id)
        if post is None:
            return {'message': 'post does not exist !'}, 400
        if LikeModel.query.filter_by(user_id=user.id, post_id=post_id).first() is not None:
            return {'message' : f'{username} has already liked this post !'}, 400
        like_object = LikeModel(True, post_id, user.id)
        LikeModel.save_to_db(like_object)
        post.total_likes += 1
        post.add_to_db()
        return {'message': f'{username} has liked post {post_id}!'}



class UnlikeAPost(Resource):
    @jwt_required()
    def post(self, username, post_id):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message':'user does not exist !'}, 400
        if user is None:
            return {'message': 'user does not exist !'}, 400
        post = PostModel.find_by_id(post_id)
        if post is None:
            return {'message': 'post does not exist !'}, 400
        like_obj =  LikeModel.query.filter_by(user_id=user.id, post_id=post.id).first()
        if like_obj is None:
            return {'message': f'post with id: {post_id} is not liked yet !'}, 400
        LikeModel.delete_from_db(like_obj)
        post.total_likes -= 1
        post.add_to_db()
        return {'message':'you have unliked the post !'}, 200
