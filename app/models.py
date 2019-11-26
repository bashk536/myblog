from app import db
from datetime import datetime

#User class inherits db.Model class: a base class for all models from Flask-SQLAlchemy
#User class defines several fields as class variables
class User(db.Model):
    id             =db.Column(db.Integer, primary_key = True)
    username       =db.Column(db.String(64), index = True, unique = True)
    email          =db.Column(db.String(120), index = True, unique = True)
    password_hash  =db.Column(db.String(128))
    posts          =db.relationship('Post', backref = 'author', lazy = 'dynamic')
    # relationship() is a high-level view of the relationship between users and posts
    #The backref argument defines the name of a field that will be added to the objects of the "many" 
    # class that points back at the "one" object.
    #  This will add a post.author expression that will return the user given a post
    # The 'lazy' argument defines how the database query for the relationship will be issued

def __repr__(self): #Tells python how to print objects of this(User) class
    return '<user {}>'.format(self.username)

class Post(db.Model):
    #####datetime.utcnow is passed as a function itself, note that it doesn't have '()'#######
    #'user' is a table name and not a class name, in some instances, model is represented by class name,
    #so keep that in mind

    id          = db.Column(db.Integer, primary_key = True)
    body        = db.Column(db.String(140))
    timestamp   = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


