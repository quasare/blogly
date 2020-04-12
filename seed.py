from models import User, Post,Tag, PostTag , db
from app import app

# Create all tables
db.drop_all()
db.create_all()

u1 = User(first_name='Mike', last_name='Johnson', image_url='https://images.unsplash.com/photo-1471119017026-179f1bb0a70e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1322&q=80')
u2 = User(first_name='Abby', last_name='Jolic', image_url='https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60')
u3 = User(first_name='Candace', last_name='Watkins', image_url='https://images.unsplash.com/photo-1535982606227-475c9bf94018?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60')

db.session.add_all([u1, u2, u3])
db.session.commit()

p1 = Post(title="Hello World", content='Hello I am a user', user_id=1)
p2 = Post(title="Kites are cool", content='I love flying kites', user_id=2)

db.session.add_all([p1,p2])
db.session.commit()

t1 = Tag(tag_name='thoughtful')
t2 = Tag(tag_name ='smart')
t3 = Tag(tag_name = 'dumb')

db.session.add_all([t1,t2, t3])
db.session.commit()

pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=2, tag_id=3)
pt3 = PostTag(post_id=1, tag_id=2)

db.session.add_all([pt1,pt2, pt3])
db.session.commit()