from flask import Blueprint
from controllers import auth_controllers

bp = Blueprint('auth_routes', __name__)




bp.route('/register',methods=['GET', 'POST'])(auth_controllers.register)
bp.route('/login',methods=['GET', 'POST'])(auth_controllers.login)
bp.route('/logout',methods=['GET','POST'])(auth_controllers.logout)

    