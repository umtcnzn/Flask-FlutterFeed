
from flask import Blueprint,current_app,render_template,session,redirect,url_for

from controllers.post_controllers import getAllPosts
from controllers.user_controllers import getSuggestedUsers

bp = Blueprint('html_routes', __name__)


@bp.route('/',methods=['GET'])
def index():
    return redirect(url_for('html_routes.home'))


@bp.route('/home',methods=['GET'])
def home():
    if "user" in session:
        URI = current_app.config.get('APP_URI')
        user = session['user']
        posts = getAllPosts()
        suggestedUsers = getSuggestedUsers()
        return render_template('home.html',user=user,posts=posts,suggestedUsers=suggestedUsers)
    return redirect(url_for('auth_routes.login'))

@bp.route('/edit_profile',methods=['GET'])
def editUserProfile():
    if 'user' not in session:
        return redirect(url_for('auth_routes.login'))
    
    loggedUser = session['user']
    return render_template('profile_edit.html',user=loggedUser)