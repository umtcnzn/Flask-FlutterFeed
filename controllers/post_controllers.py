from flask import request, jsonify,render_template,flash,session,redirect,url_for
from models.post import Post
from models.user import User
from sirope import *
import os
from werkzeug.utils import secure_filename
from controllers.comment_controllers import getComments

s = Sirope()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def viewPost(post_id):
    try:
        if 'user' not in session:
            flash("You need to be logged in to view a post.", "warning")
            return redirect(url_for('auth_routes.login'))

        postObj:Post = s.find_first(Post, lambda p: p.post_id == post_id)

        if not postObj:
            flash("Post not found!", "danger")
            return render_template('post_not_found.html')
        
        post = postObj.to_post()

        user = s.find_first(User, lambda u: u.user_id == postObj.user_id)
        comments = getComments(post_id)
        post['user'] = user.to_post()
        post['comments'] = comments

        return render_template('post.html', post=post)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))


def createPost():
    try:
        if 'user' not in session:
            flash("You need to be logged in to create a post.", "warning")
            return redirect(url_for('auth_routes.login'))

        user = session['user']
        user_id = user.get('user_id')

        content = request.form.get('content')
        if not content:
            flash("Post content cannot be empty!", "danger")
            return redirect(url_for('html_routes.home'))

        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file:
                if not allowed_file(file.filename):
                    flash("Invalid file type! Please upload a valid image file.", "danger")
                    return redirect(url_for('html_routes.home'))

                filename = secure_filename(file.filename)
                filepath = os.path.join('static/uploads/posts', filename)
                file.save(filepath)
                image = filename
      
        post = Post(
            user_id=user_id,
            text=content,
            img=image,
        )

        s.save(post)
        flash("Post created successfully!", "success")
        return redirect(url_for('html_routes.home'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))



def deletePost(post_id):
    try:
        if 'user' not in session:
            flash("You need to be logged in to delete a post.", "warning")
            return redirect(url_for('auth_routes.login'))

        postObj:Post = s.find_first(Post, lambda p: p.post_id == post_id)

        if not postObj:
            flash("Post not found!", "danger")
            return redirect(url_for('html_routes.home'))

        if postObj.user_id != session['user']['user_id']:
            flash("You are not authorized to delete this post.", "danger")
            return redirect(url_for('html_routes.home'))

        s.delete(postObj.__oid__)
        flash("Post deleted successfully!", "success")
        
        previous_page = request.referrer
        if previous_page:
            return redirect(previous_page)
        else:
            return redirect(url_for('html_routes.home'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))


def likeUnlikePost(post_id):
    try:
        if 'user' not in session:
            flash("You need to be logged in to like a post.", "warning")
            return redirect(url_for('auth_routes.login'))
        
        user = session['user']
        user_id = user.get('user_id')
        post:Post = s.find_first(Post, lambda p: p.post_id == post_id)
        if not post:
            flash("Post not found.", "danger")
            return redirect(url_for('html_routes.home'))
        
        if user_id in post.likes:
            post.likes.remove(user_id)
            flash("Post unliked successfully!", "success")
        else:
            post.likes.append(user_id)
            flash("Post liked successfully!", "success")
        
        s.save(post)
        
        previous_page = request.referrer
        if previous_page:
            return redirect(previous_page)
        else:
            return redirect(url_for('html_routes.home'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))


def getAllPosts():  
    try:
        posts = []
        iterablePosts = s.load_all(Post)
        for iterablePost in iterablePosts:
            post = iterablePost.to_post()
            user = s.find_first(User, lambda u: u.user_id == iterablePost.user_id)
            post['user'] = user.to_post() if user else None
            posts.append(post)
        sorted_posts = sorted(posts, key=lambda post: post['createdAt'], reverse=True)
        return sorted_posts
    except Exception as e:
        return {"error": str(e)}
    
def getUserPosts(user_id):  
    try:
        posts = []
        iterablePosts = s.load_all(Post)
        for iterablePost in iterablePosts:
            if iterablePost.user_id == user_id:
                post = iterablePost.to_post()
                posts.append(post)
        sorted_posts = sorted(posts, key=lambda post: post['createdAt'], reverse=True)
        return sorted_posts
    except Exception as e:
        return {"error": str(e)}