from flask import Blueprint
from controllers import user_controllers

bp = Blueprint('user_routes', __name__)

bp.route("/updateProfile",methods=['POST'])(user_controllers.updateProfile)
bp.route("/<username>",methods=['GET'])(user_controllers.getUserProfile)
bp.route("/follow/<username>",methods=['POST'])(user_controllers.followUser)
bp.route("/unfollow/<username>",methods=['POST'])(user_controllers.unfollowUser)