from flask_restful import Resource, reqparse
from models.like import LikeModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import NoResultFound

from models.post import PostModel
from models.user import UserModel

class LikeAPost(Resource):
    @jwt_required()
    def post(self, post_id):
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound:
            return {'message':'user does not exist'}, 400
        post = PostModel.find_by_id(post_id)
        if post is None:
            return {'message': 'post does not exist'}, 400
        if LikeModel.query.filter_by(user_id=user_id, post_id=post_id).first() is not None:
            return {'message' : f'{user.username} has already liked this post'}, 400
        like_object = LikeModel(True, post_id, user_id)
        LikeModel.save_to_db(like_object)
        post.total_likes += 1
        post.add_to_db()
        return {'message': f'{user.username} has liked post {post_id}!'}

class UnlikeAPost(Resource):
    @jwt_required()
    def post(self, post_id):
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound:
            return {'message':'user does not exist'}, 400
        if user is None:
            return {'message': 'user does not exist !'}, 400
        post = PostModel.find_by_id(post_id)
        if post is None:
            return {'message': 'post does not exist !'}, 400
        like_obj =  LikeModel.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like_obj is None:
            return {'message': f'post with id: {post_id} is not liked yet !'}, 400
        LikeModel.delete_from_db(like_obj)
        post.total_likes -= 1
        post.add_to_db()
        return {'message':'you have unliked the post !'}, 200
