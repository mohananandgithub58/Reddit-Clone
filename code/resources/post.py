from db import db
from models.post import PostModel
from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from datetime import datetime

from sqlalchemy.exc import NoResultFound

class CreatePost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', type = str, required = True, help = "post cannot be empty !")

    #@jwt_required()
    def post(self, username):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message':'user does not exist !'}, 400
        data = CreatePost.parser.parse_args()
        post = PostModel(content = data['content'], author_id = user.id)
        post.add_to_db()
        return {'message' : 'post created !'}, 200

class UpdatePost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', type = str, required = True, help = "post cannot be empty !")

    #@jwt_required()
    def put(self, username, post_id):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message':'user does not exist !'}, 400
        data = UpdatePost.parser.parse_args()
        for post in user.posts:
            if post.id == post_id:
                post.content = data['content']
                post.last_modified = datetime.now()
                post.add_to_db()
                return {'message':'post updated !'}, 200
        return {'message':'post not found!'}, 400

class DeletePost(Resource):
    #@jwt_required()
    def delete(self, username, post_id):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message':'user does not exist !'}, 400
        flag = 1
        for post in user.posts:
            if post.id == post_id:
                post.delete_from_db()
                flag = 0
                return {'message':'post deleted !'}, 202
        if flag == 1:
                return {'message':'Could not find post !'}, 400

class PostList(Resource):
    #@jwt_required()
    def get(self, username):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message':'user does not exist !'}, 400
        try:
            posts = user.posts
        except NoResultFound:
            return {'message': f'No active post for the user : {username}'}, 400
        data = {}
        for post in posts:
            data[post.id] = post.json()
            for comment in post.comments:
                data[post.id][comment.id] = comment.json()
        return {'posts' : data}, 200
