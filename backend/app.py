import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
from dotenv import load_dotenv
from extensions import db
from models import Comment, GlobalStats

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///angel_devil.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:password@localhost/angel_devil_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def update_stats(sentiment_score):
    stats = GlobalStats.query.first()
    if not stats:
        stats = GlobalStats(angel_power=0, devil_power=0)
        db.session.add(stats)
    
    if sentiment_score > 0:
        stats.angel_power += sentiment_score
    elif sentiment_score < 0:
        stats.devil_power += abs(sentiment_score)
    
    db.session.commit()
    return stats

@app.route('/api/comments', methods=['POST'])
def add_comment():
    data = request.json
    text = data.get('text', '')
    
    if not text or len(text) > 300:
        return jsonify({'error': 'Invalid text length'}), 400
        
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    
    # Create comment
    comment = Comment(text=text, sentiment_score=sentiment_score)
    db.session.add(comment)
    
    # Update global stats
    stats = update_stats(sentiment_score)
    
    db.session.commit()
    
    return jsonify({
        'comment': comment.to_dict(),
        'stats': stats.to_dict()
    }), 201

@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = GlobalStats.query.first()
    if not stats:
        stats = GlobalStats(angel_power=0, devil_power=0)
        db.session.add(stats)
        db.session.commit()
    return jsonify(stats.to_dict())

@app.route('/api/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.order_by(Comment.created_at.desc()).limit(10).all()
    return jsonify([c.to_dict() for c in comments])

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        # Note: In production, use migrations (Flask-Migrate)
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
            print("Make sure MySQL is running and the database exists.")
            
    app.run(debug=True, port=5000)
