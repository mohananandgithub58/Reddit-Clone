from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister, UserDelete, UserDetails, UserHomePage
from security import authentication, identity
from resources.post import CreatePost, DeletePost, PostList, UpdatePost
from resources.comments import AddCommentsToPost, DeleteAllCommentsByUserOnPost, CommentsOnPost
from resources.like import LikeAPost, UnlikeAPost

app = Flask(__name__)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'reddit_clone'

#app.secret_key='reddit_clone'
jwt = JWT(app, authentication, identity)


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

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
