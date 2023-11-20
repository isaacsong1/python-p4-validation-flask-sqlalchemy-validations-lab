from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, _, name):
        if not name:
            raise ValueError('Name is required')
        author = db.session.query(Author.id).filter_by(name = name).first()
        if author is not None:
            raise ValueError('Name is taken')
        return name
    
    @validates('phone_number')
    def validate_phone(self, _, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError('Phone number must be 10 digits')
        return phone

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

    # Add validators  
    @validates('content')
    def validate_content(self, _, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters')
        return content
    
    @validates('summary')
    def validate_summary(self, _, summary):
        if len(summary) > 250:
            raise ValueError('Summary must be less than 250 characters')
        return summary
    
    @validates('category')
    def validate_category(self, _, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be Fiction or Non-Fiction')
        return category
    
    @validates('title')
    def validate_title(self, _, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError("Title is required")
        if not any([bait in title for bait in clickbait]):
            raise ValueError('Title must contain a clickbait')
        return title
        

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
