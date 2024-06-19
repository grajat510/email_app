from flask_login import UserMixin
from app.extensions import bcrypt

class User(UserMixin):
    def __init__(self, email, password, _id):
        self.email = email
        self.password = password
        self.id = _id

    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)
