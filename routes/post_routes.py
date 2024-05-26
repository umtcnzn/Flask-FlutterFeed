from flask import Blueprint
from controllers import post_controllers

bp = Blueprint('post_routes', __name__)

bp.route('/post/<post_id>',methods=['GET'])(post_controllers.viewPost)
bp.route('/createPost',methods=['POST'])(post_controllers.createPost)
bp.route('/deletePost/<post_id>',methods=['POST'])(post_controllers.deletePost)
bp.route('/likeUnlikePost/<post_id>',methods=['POST'])(post_controllers.likeUnlikePost)