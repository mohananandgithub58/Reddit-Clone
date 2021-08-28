from models.blocklist import TokenBlockListModel
from flask_restful import Resource
from datetime import datetime

class Logout(Resource):
    def add_to_blocklist(self):
        TokenBlockListModel.logout(self)


class CheckBloackedUsers():
    def check_for_blocked_user(jti):
        token = TokenBlockListModel.find_by_jti(jti)
        if token is None:
            return True
        if token.get_revoked_status() == 1:
            return True
        else:
            return False
