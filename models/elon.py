from models import db
from datetime import datetime

class Elon(db.Model):
    __tablename__ = "announcement"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    category_id = db.Column(db.Integer(), nullable=False)
    image_url = db.Column(db.Text(), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_id, title, description, price, category_id, image_url):
        super().__init__()
        self.user_id = user_id
        self.title = title
        self.description = description
        self.price = price
        self.category_id = category_id
        self.image_url = image_url

    def to_dict(self):
        elon_data = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "category_id": self.category_id,
            "image_url": self.image_url,
            "created_at": str(self.created_at)
        }

        return elon_data
