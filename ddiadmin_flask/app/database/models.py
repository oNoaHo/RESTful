from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Document):
    name = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=12)
