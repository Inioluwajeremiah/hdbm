
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func


class HdbModel(db.Model):
    __bind_key__ = 'students_records'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    middlename = db.Column(db.String(50))
    department = db.Column(db.String(50))
    course = db.Column(db.String(50))
    level = db.Column(db.String(50))
    hallname = db.Column(db.String(50))
    blockname = db.Column(db.String(50))
    roomno = db.Column(db.String(50))
    dateTime = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)


class AdminModel(UserMixin, db.Model):
    __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    hashedPassword = db.Column(db.String(150), index=True)

    # def set_password(self, password):pyt
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
