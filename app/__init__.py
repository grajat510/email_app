from flask import Flask
from app.extensions import bcrypt, login_manager, mongo
from bson import ObjectId
from app.models import User
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mongo.init_app(app)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(email=user_data['email'], password=user_data['password'], _id=user_data['_id'])
    return None
