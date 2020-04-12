"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post,Tag,  PostTag ,  friendly_date

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# Home
@app.route('/')
def render_home():
    post = Post.query.order_by(Post.created_at.desc()).limit('5').all()
    return render_template('home.html', post=post)

# Users List
@app.route('/users')
def render_users_List():
    users = User.query.all()
    return render_template('users/users_list.html', users=users)

# Create new user
@app.route('/users/new')
def add_user_form():
    return render_template('users/user_form.html')   

@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['img_url'] 

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')   

# Render User details
@app.route('/user/<user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/details.html', user = user)

# Edit User
@app.route('/user/<user_id>/edit')
def edit_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit_user.html', user = user)    

@app.route('/user/<user_id>/edit', methods=["POST"])
def post_edit_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['img_url'] 

    db.session.add(user)
    db.session.commit()

    return redirect('/users')       

# Delete user
@app.route('/user/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


# Add a new Post
@app.route('/user/<user_id>/posts/new')
def user_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/post_form.html', user=user, tags=tags)

@app.route('/user/<user_id>/posts/new', methods=['POST'])
def submit_post_form(user_id):
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/user/{user_id}')

# Render Post
@app.route('/posts/<post_id>')
def render_posts(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('posts/post_details.html', post=post)    

# Edit Post
@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit_post.html', post=post, tags=tags)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def submit_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content'] 

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f'/user/{post.user_id}')

# Delete a Post
@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')

# List Tags
@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)

# Render Tag Details
@app.route('/tags/<tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)    
    return render_template('tag_detail.html', tag=tag)

# Add new tag
@app.route('/tags/new')
def add_tag():
    return render_template('tag_form.html')

@app.route('/tags/new', methods=['POST'])
def submit_tag():
    tag_name = request.form['tag_name']
    new_tag = Tag(tag_name=tag_name)
    
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.tag_name = request.form['tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tag_id>/delete', methods=['POST']) 
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')   