from flask_login import current_user
from models import User,Questions

class Analysis:
    def __init__(self):
        a = Questions.query.filter(student = current_user.id)
        print(a)

Analysis()