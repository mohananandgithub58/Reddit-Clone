from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity, get_jti
from flask import jsonify
from datetime import timedelta
from flask_jwt_extended.config import config

from resources.user import *
from resources.post import *
from resources.comments import *
from resources.like import *
from resources.BlockList import *

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = '#reddit_clone#'
app.config['JWT_SECRET_KEY'] = '#reddit_app_jwt_super_secret_ec5cpu@ANAND5#'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=10)
app.config['JWT_BLACKLIST_ENABLED'] = True

jwt = JWTManager()
jwt.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_headers, jwt_payload):
    jti = jwt_payload['jti']
    x=  CheckBloackedUsers.check_for_blocked_user(jti)
    print('status', x)
    return x


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
api.add_resource(UserDelete, '/deleteuser')
api.add_resource(UserDetails, '/userdetails')
api.add_resource(UserHomePage, '/userhomepage')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

api.add_resource(CreatePost, '/createpost')
api.add_resource(DeletePost, '/deletepost/<int:post_id>')
api.add_resource(PostList, '/postlist')
api.add_resource(UpdatePost, '/updatepost/<int:post_id>')
api.add_resource(AddCommentsToPost, '/addcomment')
api.add_resource(DeleteAllCommentsByUserOnPost,'/deletecommentsonpost')
api.add_resource(CommentsOnPost, '/comments/<int:post_id>')

api.add_resource(LikeAPost, '/likepost/<int:post_id>')
api.add_resource(UnlikeAPost, '/unlikepost/<int:post_id>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
