from db import db
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy.exc import NoResultFound

from models.post import PostModel
from models.user import UserModel

class CreatePost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', type = str, required = True, help = "post cannot be empty")

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound as e:
            return {'message':'user not found'}, 400
        data = CreatePost.parser.parse_args()
        post = PostModel(content = data['content'], author_id = user_id)
        post.add_to_db()
        return {'message' : 'post created'}, 201

class UpdatePost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', type = str, required = True, help = "post cannot be empty !")

    @jwt_required()
    def put(self, post_id):
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound as e:
            return {'message':'user not found'}, 400
        data = UpdatePost.parser.parse_args()
        for post in user.posts:
            if post.id == post_id:
                post.content = data['content']
                post.last_modified = datetime.now()
                post.add_to_db()
                return {'message':'post updated'}, 200
        return {'message':'post not found'}, 400

class DeletePost(Resource):
    @jwt_required()
    def delete(self, post_id):
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound as e:
            return {'message':'user not found'}, 400
        flag = 1
        for post in user.posts:
            if post.id == post_id:
                post.delete_from_db()
                flag = 0
                return {'message':'post deleted'}, 202
        if flag == 1:
                return {'message':'could not find post'}, 400

class PostList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound as e:
            return {'message':'user not found'}, 400
        try:
            posts = user.posts
        except NoResultFound:
            return {'message': 'no active post for the user'}, 400
        data = {}
        for post in posts:
            data[post.id] = post.json()
            for comment in post.comments:
                data[post.id][comment.id] = comment.json()
        return {'posts' : data}, 200
