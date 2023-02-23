from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from project.models import db
import berserk
import os


app = Flask(__name__)
app.config.from_object("project.config.Config")
db.init_app(app)


api_key = os.environ.get("API_TOKEN")
session = berserk.TokenSession(api_key)
client = berserk.Client(session=session)

# blueprint for auth routes in our app
from .crud import crud as crud_blueprint
app.register_blueprint(crud_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .youtubeTimeStamps import youtubeTimeStamps as youtubeTimeStamps_blueprint
app.register_blueprint(youtubeTimeStamps_blueprint)

from .overview import overview as overview_blueprint
app.register_blueprint(overview_blueprint)
