from flask_login import UserMixin
from . import db


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    student_class = db.Column(db.String(10))
    board = db.Column(db.String(100))
    state = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(1000))
    qs = db.relationship('Questions')

class Questions(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question = db.Column(db.Integer)
    choice = db.Column(db.Integer)
    student = db.Column(db.Integer,db.ForeignKey('user.id'))





