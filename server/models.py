from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('name')
    def validate_name(self, key, name):
     if not name:
        raise ValueError('Name must be provided')
     return name
 
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            return None  # Allow null phone numbers
        # Remove non-digit characters and check length
        phone_number_digits = re.sub(r'\D', '', phone_number)
        if len(phone_number_digits) != 10:
            raise ValueError('Phone number must be exactly ten digits long')
        return phone_number
     
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self,key,content):
        if len(content) < 250:
            raise ValueError('content must be atleast 255 characters long')
    
        return content
    
    @validates('summary')
    def validates_summary(self,key,summary):
        if len(summary) > 250:
            raise ValueError('summary should be >=250')
        return summary
    
    @validates('category')
    def validate_category(self,key,category):
        if category not in['fiction','non-fiction']:
          raise ValueError('category must be either fiction or non fiction')
        return category
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Post title must contain one of the following phrases: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title
