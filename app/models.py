from app import app, db, login
from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

followers = db.Table( 'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

#User class inherits db.Model class: a base class for all models from Flask-SQLAlchemy
#User class defines several fields as class variables
class User(UserMixin, db.Model):
    id             =db.Column(db.Integer, primary_key = True)
    username       =db.Column(db.String(64), index = True, unique = True)
    email          =db.Column(db.String(120), index = True, unique = True)
    password_hash  =db.Column(db.String(128))
    posts          =db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me       =db.Column(db.String(140))
    last_seen      =db.Column(db.DateTime, default=datetime.utcnow)
    followed       =db.relationship(
                    'User', secondary=followers,
                    primaryjoin=(followers.c.follower_id == id),
                    secondaryjoin=(followers.c.followed_id == id),
                    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
                    
    liked          =db.relationship(
                    'PostLike',
                    foreign_keys='PostLike.user_id',
                    backref='user', lazy='dynamic')

    
    # relationship() is a high-level view of the relationship between users and posts
    #The backref argument defines the name of a field that will be added to the objects of the "many" 
    # class that points back at the "one" object.
    #  This will add a post.author expression that will return the user given a post
    # The 'lazy' argument defines how the database query for the relationship will be issued

    def __repr__(self): #Tells python how to print objects of this(User) class
        return '<user {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size) 

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    #####datetime.utcnow is passed as a function itself, note that it doesn't have '()'#######
    #'user' is a table name and not a class name, in some instances, model is represented by class name,
    #so keep that in mind

    id          = db.Column(db.Integer, primary_key = True)
    body        = db.Column(db.String(140))
    timestamp   = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes       = db.relationship('PostLike', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

