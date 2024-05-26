from flask import request, jsonify,render_template,flash,session,redirect,url_for
from models.user import User
from sirope import *
from werkzeug.utils import secure_filename
import os

s = Sirope()


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
from controllers.post_controllers import getUserPosts


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def updateProfile():
    try:
        if 'user' not in session:
            flash("You need to be logged in to update your profile.", "warning")
            return redirect(url_for('auth_routes.login'))

        loggedUser = session['user']
        user = s.find_first(User, lambda u: u.user_id == loggedUser['user_id'])

        if not user:
            flash("User not found!", "danger")
            return redirect(url_for('html_routes.home'))

        if request.method == 'POST':
            name = request.form.get('name')
            username = request.form.get('username')
            email = request.form.get('email')
            bio = request.form.get('bio')
            profile_image = None

            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join('static/uploads/profiles', filename)
                    file.save(filepath)
                    profile_image = filename

            if username != loggedUser['username']:
                if s.find_first(User, lambda u: u.username == username):
                    flash("Username already taken!", "danger")
                    return redirect(url_for('html_routes.editUserProfile'))

            if email != loggedUser['email']:
                if s.find_first(User, lambda u: u.email == email):
                    flash("E-mail already taken!", "danger")
                    return redirect(url_for('html_routes.editUserProfile'))

            user.name = name
            user.username = username
            user.email = email
            user.bio = bio
            if profile_image:
                user.profilePic = profile_image

            s.save(user)
            session['user'] = user.to_dict()
            flash("Profile updated successfully!", "success")

        return redirect(url_for('html_routes.home'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))
    
def getUserProfile(username):
    try:
        if not 'user' in session:
            flash("You need to be logged in to view user profiles.", "warning")
            return redirect(url_for('auth_routes.login'))
        
        user:User = s.find_first(User, lambda u: u.username == username)

        if not user:
            flash("User not found!", "danger")
            return render_template('user_not_found.html')
        
        loggedUser:User = s.find_first(User,lambda u: u.username == session['user']['username'])
        isFollowing = loggedUser.user_id in user.followers
        userPosts = getUserPosts(user.user_id)
        
        return render_template('profile.html', user=user.to_dict(), isFollowing=isFollowing, posts=userPosts)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))



def followUser(username):
    try:
        if not 'user' in session:
            flash("You need to be logged in to follow users.", "warning")
            return redirect(url_for('auth_routes.login'))
        
        user:User = s.find_first(User, lambda u: u.username == username)
        loggedUser = s.find_first(User, lambda u: u.username == session['user']['username'])
        
        user.followers.append(loggedUser.user_id)
        loggedUser.following.append(user.user_id)

        s.save(user)
        s.save(loggedUser)
        
        flash(user.username + ' succesfully followed!','success')

        previous_page = request.referrer
        if previous_page:
            return redirect(previous_page)
        else:
            return redirect(url_for('html_routes.home'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))


def unfollowUser(username):
    try:
        if not 'user' in session:
            flash("You need to be logged in to unfollow users.", "warning")
            return redirect(url_for('auth_routes.login'))
        
        user:User = s.find_first(User, lambda u: u.username == username)
        loggedUser = s.find_first(User, lambda u: u.username == session['user']['username'])

        user.followers.remove(loggedUser.user_id)
        loggedUser.following.remove(user.user_id)
        
        s.save(user)
        s.save(loggedUser)
        flash(user.username + ' succesfully unfollowed!','success')

        previous_page = request.referrer
        if previous_page:
            return redirect(previous_page)
        else:
            return redirect(url_for('html_routes.home'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))


def getSuggestedUsers():
    try:
        users = s.load_all(User)
        suggestedUsers = []
        loggedUser = session['user']
        for user in users:
            if user.user_id != loggedUser['user_id'] and (loggedUser['user_id'] not in user.followers):
                suggestedUsers.append(user.to_post())
            if len(suggestedUsers) == 3:
                break
        return suggestedUsers
    except Exception as e:
        return {"error": str(e)}
