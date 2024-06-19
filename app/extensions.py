from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pymongo import PyMongo

bcrypt = Bcrypt()
login_manager = LoginManager()
mongo = PyMongo()
