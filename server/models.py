from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


"""
## Basic Validations

Add validators to the `Author` and `Post` models such that:

1. All authors have a name.
2. No two authors have the same name.
3. Author phone numbers are exactly ten digits.
4. Post content is at least 250 characters long.
5. Post summary is a maximum of 250 characters.
6. Post category is either `Fiction` or `Non-Fiction`.
7. Post title is sufficiently clickbait-y and must contain one of the following:
   - "Won't Believe"
   - "Secret"
   - "Top"
   - "Guess"

You should not need to run another migration, unless you altered model
constraints.

Run `pytest -x` to run your tests. Use these instructions and `pytest`'s error
messages to complete your work in the `server/` folder.
"""

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name field is required.")
        author = db.session.query(Author.id).filter_by(name = name).first()
        if author is not None:
            raise ValueError("Name must be unique.")
        return name
    
    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        return phone_number

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
    
    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError ("Title field is required.")
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title
    
    @validates("content", "summary")
    def validate_length(self, key, string):
        if ( key == "content"):
            if len(string) < 250:
                raise ValueError("Post content must be greater than or equal 250 characters long.")
        if ( key == "summary"):
            if len(string) > 250:
                raise ValueError("Post summary must be less than or equal to 250 characters long.")
        return string
    
    @validates("category")
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
    
    
