from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class users(db.Document):
    userid = db.StringField(required=True, unique=True)
    email = db.StringField()
    department = db.StringField()
    firstname = db.StringField()
    lastname = db.StringField()
    networks = db.ListField()
    zones = db.ListField()
    records = db.ListField()
    groups = db.ListField()


class groups(db.Document):
    name = db.StringField(required=True, unique=True)
    email = db.StringField()
    comment = db.StringField()
    networks = db.ListField()
    zones = db.ListField()
    records = db.ListField()


class apiuser(db.Document):
    # email = db.EmailField(required=True, unique=True)
    name = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
