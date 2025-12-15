from extensions import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'sentiment_score': self.sentiment_score,
            'created_at': self.created_at.isoformat()
        }

class GlobalStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angel_power = db.Column(db.Float, default=0.0)
    devil_power = db.Column(db.Float, default=0.0)
    
    def to_dict(self):
        return {
            'angel_power': self.angel_power,
            'devil_power': self.devil_power
        }
