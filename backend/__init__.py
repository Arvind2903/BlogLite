from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_login import LoginManager
from flask_security import Security
from flask_caching import Cache

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/api/user"
CORS(app)
app.app_context().push()

from backend.config import LocalDevelopmentConfig
app.config.from_object(LocalDevelopmentConfig)

cache = Cache(app)
app.app_context().push()

from backend.api import *
api = Api(app)

from backend.models import *
security = Security(app, user_datastore)
ma.init_app(app)

from backend.database import db
db.init_app(app)
app.app_context().push()
db.create_all()
api.add_resource(PostsApi, "/api/posts", "/api/posts/<int:user_id>")
api.add_resource(UserPostsApi, "/api/userposts", "/api/userposts/<int:id>")
api.add_resource(SignUpApi, "/api/signup")
api.add_resource(UserApi, "/api/user", "/api/user/<int:id>")
api.add_resource(LogoutApi, "/api/logout")
api.add_resource(FollowersApi, '/api/followers/<int:id>')
api.add_resource(FollowingsApi, '/api/followings/<int:id>')
api.add_resource(ActivityApi, '/api/activity')
api.add_resource(JobApi, '/api/job')

from backend.workers import celery, ContextTask
celery.conf.update(
    broker_url = app.config["CELERY_BROKER_URL"],
    result_backend = app.config["CELERY_RESULT_BACKEND"]
)
celery.conf.enable_utc = False
celery.conf.timezone = "Asia/Calcutta"
celery.Task = ContextTask
app.app_context().push()

import backend.tasks

