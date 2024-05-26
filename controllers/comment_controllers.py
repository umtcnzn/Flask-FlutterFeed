from flask import request, jsonify,render_template,flash,session,redirect,url_for
from models.comment import Comment
from models.post import Post
from models.user import User
from sirope import *

s = Sirope()

def createComment(post_id):
    if 'user' not in session:
        flash("You need to be logged in to comment.", "warning")
        return redirect(url_for('auth_routes.login'))

    user_id = session['user']['user_id']
    text = request.form.get('comment')

    if not text:
        flash("comment text cannot be empty.", "danger")
        return redirect(url_for('post_routes.viewPost',post_id=post_id))

    try:
        postObj = s.find_first(Post, lambda p: p.post_id == post_id)
        if not postObj:
            flash("Post not found!", "danger")
            return redirect(url_for('post_routes.viewPost',post_id=post_id))
    except:
        flash("An error occurred while finding the post.", "danger")
        return redirect(url_for('post_routes.viewPost',post_id=post_id))

    new_comment = Comment(user_id=user_id, post_id=post_id, text=text)

    s.save(new_comment)
    flash("Comment created successfully!", "success")
    return redirect(url_for('post_routes.viewPost',post_id=post_id))

def likeUnlikeComment(comment_id):
    if 'user' not in session:
        flash("You need to be logged in to like or unlike a comment.", "warning")
        return redirect(url_for('auth_routes.login'))

    comment = s.find_first(Comment, lambda c: c.comment_id == comment_id)

    if not comment:
        flash("Comment not found!", "danger")
        return redirect(url_for('html_routes.home'))

    user_id = session['user']['user_id']
    
    if user_id in comment.likes:
        comment.likes.remove(user_id)
        flash("You unliked the comment.", "success")
    else:
        comment.likes.append(user_id)
        flash("You liked the comment.", "success")
    
    s.save(comment)

    previous_page = request.referrer
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect(url_for('html_routes.home'))

def deleteComment(comment_id):
    if 'user' not in session:
        flash("You need to be logged in to delete a comment.", "warning")
        return redirect(url_for('auth_routes.login'))

    commentObj = s.find_first(Comment, lambda c: c.comment_id == comment_id)

    if not commentObj:
        flash("Comment not found!", "danger")
        return redirect(url_for('html_routes.home'))

    if commentObj.user_id != session['user']['user_id']:
        flash("You are not authorized to delete this comment.", "danger")
        return redirect(url_for('html_routes.home'))

    try:
        s.delete(commentObj.__oid__)
        flash("Comment deleted successfully!", "success")
    except Exception as e:
        flash("An error occurred while deleting the comment.", "danger")
        print(f"Error deleting comment: {e}")

    previous_page = request.referrer
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect(url_for('html_routes.home'))

def getComments(post_id):
    try:
        comments = []
        iterableComments = s.load_all(Comment)
        for iterableComment in iterableComments:
            if post_id == iterableComment.post_id:
                comment = iterableComment.to_post()
                user = s.find_first(User,lambda u: u.user_id == iterableComment.user_id)
                comment['user'] = user.to_post() if user else None
                comments.append(comment)
        sorted_comments = sorted(comments, key=lambda comment: comment['createdAt'], reverse=True)
        return sorted_comments
    except Exception as e:
        return {"error": str(e)}
    
