from models import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = "category"


    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, title, description):
        super().__init__()
        self.title = title
        self.description = description

    def to_dict(self):
        category_data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": str(self.created_at)
        }

        return category_data
        
        