from app import db
from datetime import datetime

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    headline = db.Column(db.String(100), nullable=False)
    excerpt = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return {
            'id': self.id,
            'date': self.date,
            'headline': self.headline,
            'excerpt': self.excerpt,
            'content': self.content,
        }