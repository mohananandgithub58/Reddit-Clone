from app import app
from datetime import timedelta
from flask_jwt_extended.config import config
ACCESS_EXPIRES = timedelta(hours=1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '#reddit_clone#'
app.config['JWT_SECRET_KEY'] = '#reddit_app_jwt_super_secret_ec5cpu@ANAND5#'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config['JWT_BLACKLIST_ENABLED'] = True
