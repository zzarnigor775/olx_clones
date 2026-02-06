from models import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100),nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, fullname, username, password, role):
        super().__init__()
        self.fullname = fullname
        self.username = username
        self.password = password
        self.role = role
        
    def to_dict(self):
        user_data = {
            "id": self.id,
            "fullname": self.fullname,
            "username": self.username,
            "role": self.role,
            "created_at": str(self.created_at)
        }
        return user_data
