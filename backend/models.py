from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(255))
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    surname = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    home_address = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    facebook_username = db.Column(db.String(100))
    twitter_username = db.Column(db.String(100))
    instagram_username = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.first_name} {self.surname}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'surname': self.surname,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d'),
            'facebook_username': self.facebook_username,
            'twitter_username': self.twitter_username,
            'instagram_username': self.instagram_username,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }