from datetime import datetime
from pictures import db

class ImageFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(120), default=datetime.utcnow)
    image_file = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.image_file}')"
