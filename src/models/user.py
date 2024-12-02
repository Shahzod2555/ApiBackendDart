from ..extends import db
from flask_login import UserMixin
from ..extends import login_manager

@login_manager.user_loader
def load_user(id_uses):
  return db.session.get(User, int(id_uses))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    phone_number = db.Column(db.String(12), unique=True, nullable=True)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<User {self.email or self.phone_number}>"

    def __init__(self, email, password, phone_number):
        self.phone_number = phone_number
        self.email = email
        self.password = password

