from flask_restful import Resource
from datetime import datetime
from flask_jwt_extended import jwt_required

from models.blocklist import TokenBlockListModel

class Logout():
    @jwt_required()
    def add_to_blocklist(self):
        TokenBlockListModel.logout(self)

class CheckUserLoggedInStatus():
    def check_user_loggedin_status(id):
        user = TokenBlockListModel.find_by_userid(id)
        if user is None:
            return None
        else:
            return user.get_revoked_status()

class CheckBloackedUsers():
    def check_for_blocked_user(jti):
        token = TokenBlockListModel.find_by_jti(jti)
        if token is None or token.get_revoked_status()== 1:
            return True
        else:
            return False
