from models.comments import CommentsModel
from db import db
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from datetime import datetime
from models.user import UserModel
from models.post import PostModel
from models.comments import CommentsModel

from sqlalchemy.exc import NoResultFound

class AddCommentsToPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content', type=str, required=True, help="post cannot be empty !")
    parser.add_argument('post_id', type=int, required=True, help="comment must have a post id !")

    @jwt_required()
    def post(self, username):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message' : 'user does not exist !'}, 400
        data = AddCommentsToPost.parser.parse_args()
        if PostModel.find_by_id(data['post_id']) is None:
            return {'message':'post does not exist !'}, 400
        comment = CommentsModel(user.id, data['post_id'], data['content'])
        comment.save_to_db()
        return {'message': 'comment is successfully added'}, 200

class DeleteAllCommentsByUserOnPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('post_id', type=int, required=True, help="comment must have a post id !")

    @jwt_required()
    def delete(self, username):
        try:
            user = UserModel.find_by_username(username)
        except NoResultFound:
            return {'message': 'user does not exist !'}, 400
        data = DeleteAllCommentsByUserOnPost.parser.parse_args()
        if PostModel.find_by_id(data['post_id']) is None:
            return {'message': 'post does not exist !'}, 400
        comments_list = CommentsModel.query.filter_by(user_id=user.id, post_id=data['post_id'])
        if comments_list.count() > 0:
            for comment in comments_list:
                db.session.delete(comment)
            db.session.commit()
            return {'message': f'all comments by <{username}> on post id:{data["post_id"]} are deleted !'}, 200
        else:
            return {'message' : f'no comment exist on post {data["post_id"]} by user : <{username}>'}, 400

class CommentsOnPost(Resource):
    @jwt_required()
    def get(self, post_id):
        try:
            post = PostModel.find_by_id(post_id)
        except NoResultFound:
            return {'message':'post does not exist !'}, 400
        else:
            return {'comments ': list(map(lambda x: x.json(), post.comments))}


class UpdateComment(Resource):
    pass



class LoadAllCommentsOfPost(Resource):
    pass
