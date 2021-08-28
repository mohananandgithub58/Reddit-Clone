from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity, get_jti
from flask import jsonify

from resources.user import *
from resources.post import *
from resources.comments import *
from resources.like import *
from resources.BlockList import *
from datetime import timedelta
from flask_jwt_extended.config import config

app = Flask(__name__)
api = Api(app)

ACCESS_EXPIRES = timedelta(hours=1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '#reddit_clone#'
app.config['JWT_SECRET_KEY'] = '#reddit_app_jwt_super_secret_ec5cpu@ANAND5#'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager()
jwt.init_app(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_headers, jwt_payload):
    jti = jwt_payload['jti']
    return CheckBloackedUsers.check_for_blocked_user(jti)


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description' : 'signature varification failed',
        'error' : 'invalid token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 2:
        return {'is_admin':True,'is_logged_out': False}
    else:
        return {'is_admin':False,'is_logged_out': False}

api.add_resource(UserRegister, '/register')
api.add_resource(UserDelete, '/deleteuser/<string:username>')
api.add_resource(UserDetails, '/userdetails/<string:username>')
api.add_resource(CreatePost, '/<string:username>/createpost')
api.add_resource(DeletePost, '/<string:username>/deletepost/<int:post_id>')
api.add_resource(PostList, '/postlist/<string:username>')
api.add_resource(UpdatePost, '/<string:username>/updatepost/<int:post_id>')
api.add_resource(AddCommentsToPost, '/<string:username>/addcomment')
api.add_resource(DeleteAllCommentsByUserOnPost,'/<string:username>/deletecommentsonpost')
api.add_resource(CommentsOnPost, '/comments/<int:post_id>')
api.add_resource(UserHomePage, '/userhomepage')
api.add_resource(LikeAPost, '/<string:username>/likepost/<int:post_id>')
api.add_resource(UnlikeAPost, '/<string:username>/unlikepost/<int:post_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)



# @jwt.revoked_token_loader
# def revoked_token_response(jwt_header, jwt_payload):
#     jti = jwt_payload['jti']
#     print(jti)
#     AddToBlockList.add_to_blocklist(jti)
#     return {'revioked'}



# @jwt.needs_fresh_token_loader
# def token_not_fresh_callback():
#     return jsonify({
#         'description': 'The token is not fresh.',
#         'error': 'fresh token required'
#     }), 401


# @jwt.revoked_token_loader
# def revoked_token_callback():
#     return jsonify({
#         'description': 'The token has been revoked.',
#         'error': 'token_revoked'
#     }), 401
