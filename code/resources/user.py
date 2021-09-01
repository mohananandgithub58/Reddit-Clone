from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_current_user, get_jti
from flask import jsonify
from werkzeug.security import safe_str_cmp
import re
from sqlalchemy.exc import NoResultFound
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)


from models.user import UserModel
from models.post import PostModel
from models.blocklist import TokenBlockListModel
from models.comments import CommentsModel
from models.like import LikeModel
from models.user import UserModel
from resources.post import PostList

from resources.BlockList import Logout, CheckUserLoggedInStatus


class UserLogin(Resource):
    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('username', type = str, required = True, help = "username is mandatory !!")
    _user_parser.add_argument('password', type = str, required = True, help = "password is mandatory !!")

    @classmethod
    def post(cls):
        data = cls._user_parser.parse_args()
        try:
            user = UserModel.find_by_username(data['username'])
        except NoResultFound:
            return {'message':'user does not exist'}, 400
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            block_list = TokenBlockListModel.find_by_userid(user.id)
            if block_list:
                block_list.update_block_list(get_jti(access_token), get_jti(refresh_token))
            else:
                loggin_status = TokenBlockListModel(user.id, get_jti(access_token), get_jti(refresh_token))
                TokenBlockListModel.add_to_db(loggin_status)
            return {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token
                   }, 200
        else:
            return {'message':'invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound:
            return {'message':'user does not exist'}, 400
        user_obj = TokenBlockListModel.find_by_userid(user_id)
        TokenBlockListModel.logout(user_obj)
        return {'message':'user successfully loggout out'}, 200

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        user_obj = TokenBlockListModel.find_by_userid(current_user)
        user_obj.set_jti(get_jti(new_token))
        return {'access_token': new_token}, 200

class UserRegister(Resource):
    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('username', type = str, required = True, help = "username is mandatory !!")
    _user_parser.add_argument('password', type = str, required = True, help = "password is mandatory !!")

    def post(self):
        data = UserRegister._user_parser.parse_args()
        try:
            user = UserModel.find_by_username(data['username'])
        except NoResultFound:
            password = data['password']
            password_validation = 0
            if len(password) < 8:
                return {'message' : 'password must be minimum 8 characters long'}, 400
            if UserModel.validate_password(password) is False:
                return {'message': 'password must contain alphabets, numbers, atlest one speceial and uppercase character !'}, 400
            user = UserModel(**data)
            user.save_to_db()
            return {'message':'user registration successfully'}, 201
        else:
            username = data['username']
            return {'message': f'user with {username} already exist'}, 400

class UserDetails(Resource):
    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('name', type = str, required = False)
    _user_parser.add_argument('about', type = str, required = False)

    @jwt_required()
    def post(self):

        data = UserDetails._user_parser.parse_args()
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound as e:
            return {'message':'user not found'}, 400
        if data['about'] != None:
            user.about = data['about']
        if data['name'] != None:
            user.name = data['name']
        user.save_to_db()
        return {'message' : 'user data updated successfully'}, 201

    @jwt_required()
    def get(self):
        data = UserDetails._user_parser.parse_args()
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound as e:
            return {'message':'user not found'}, 400
        if CheckUserLoggedInStatus.check_user_loggedin_status(user_id) is None or False:
            return {'message':'user is not logged in'}, 400
        return {'message' : f'Name: {user.name}, About : {user.about}'}, 200

class UserDelete(Resource):
    @jwt_required(fresh=True)
    def delete(self):
        # claims = get_jwt()
        # if not claims['is_admin']:
        #     return {'message':'admin previlage required !'}, 401
        # print(claims['is_admin'])
        user_id = get_jwt_identity()
        try:
            user = UserModel.find_by_id(user_id)
        except NoResultFound as e:
            return {'message':'user not found'}, 400
        likes_on_any_post = LikeModel.query.filter_by(user_id=user_id).all()
        for likes in likes_on_any_post:
            likes.post.total_likes -= 1
            likes.post.add_to_db()
            likes.delete_from_db()
        user.delete_from_db()
        return {'message':'user deleted succussfully'}, 200

class UserHomePage(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        try:
            posts = PostModel.query.order_by(PostModel.last_modified.desc())
            user = UserModel.find_by_id(user_id)
        except NoResultFound:
            return {'message':'posts are not posted yet or invalid user'}, 400
        if user_id:
            data = {}
            for post in posts:
                data[post.id] = post.json()
                for comment in post.comments:
                    data[post.id][comment.id] = comment.json()
            return {'recent posts ': data}, 200
        else:
            return {
                'posts': [post.json() for post in posts],
                'message':'more data available if you login'
            }, 200
