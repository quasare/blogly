"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(15),
                     nullable=False)

    last_name = db.Column(db.String(15),
                     nullable=False)

    image_url = db.Column(db.String, nullable=True, unique=True)   

    posts = db.relationship('Post', backref='User', cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"<User id={u.id} name={u.first_name} {u.last_name}>"

class Post(db.Model): 

    __tablename__= 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String, nullable=False)

    content = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Tag(db.Model):

    __tablename__='tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    tag_name = db.Column(db.String, nullable=False, unique=True)

    post_tag = db.relationship('Post', secondary='post_tags', backref='tags')

class PostTag(db.Model):

    __tablename__='post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)  

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)   


def friendly_date():
    post = Post.query.order_by(Post.created_at.desc()).limit('5').all()
    for p in post:
        conv_date = p.created_at.strftime('%c')
    return True

 

