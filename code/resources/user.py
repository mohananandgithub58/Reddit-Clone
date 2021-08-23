from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
import re

from models.post import PostModel
from models.comments import CommentsModel
from resources.comments import LoadAllCommentsOfPost
from resources.post import PostList
from models.like import LikeModel
from models.user import UserModel

from sqlalchemy.exc import NoResultFound

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type = str, required = True, help = "username is mandatory !!")
    parser.add_argument('password', type = str, required = True, help = "password is mandatory !!")


    def post(self):
        data = UserRegister.parser.parse_args()
        password = data['password']
        password_validation = 0
        if len(password) < 8:
            return {'message' : 'password must be minimum 8 characters long'}
        if UserModel.validate_password(password) is False:
            return {'message': 'password must contain alphabets, numbers, atlest one speceial and uppercase character !'}, 400
        user = UserModel(**data)
        return user.save_to_db()

class UserDetails(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type = str, required = False)
    parser.add_argument('about', type = str, required = False)

    #@jwt_required()
    def post(self, username):
        data = UserDetails.parser.parse_args()
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound as e:
            return {'message':'user does not exist !'}, 400
        if data['about'] != None:
            user.about = data['about']
        if data['name'] != None:
            user.name = data['name']
        user.save_to_db()
        return {'message' : 'user data updated successfully !'}, 201

    #@jwt_required()
    def get(self, username):
        data = UserDetails.parser.parse_args()
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound as e:
            return {'message':'user does not exist !'}, 400
        return {'message' : f'Name: {user.name}, About : {user.about}'}, 200


class UserDelete(Resource):
    #@jwt_required()
    def delete(self, username):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message' : 'user does not exist !'}, 400
        likes_on_any_post = LikeModel.query.filter_by(user_id=user.id).all()
        for likes in likes_on_any_post:
            likes.post.total_likes -= 1
            likes.post.add_to_db()
            likes.delete_from_db()
        user.delete_from_db()
        return {'message':'User deleted Succussfully !'}, 200


class UserHomePage(Resource):
    #@jwt_required()
    def get(self):
        try:
            posts = PostModel.query.order_by(PostModel.last_modified.desc())
        except NoResultFound:
            return {'message':'Posts are not posted yet !'}
        data = {}
        for post in posts:
            data[post.id] = post.json()
            for comment in post.comments:
                data[post.id][comment.id] = comment.json()
        return {'recent posts ': data}, 200
