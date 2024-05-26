from flask import Blueprint
from controllers import comment_controllers

bp = Blueprint('comment_routes', __name__)


bp.route("/createComment/<post_id>",methods=['POST'])(comment_controllers.createComment)
bp.route("/likeUnlikeComment/<comment_id>",methods=['POST'])(comment_controllers.likeUnlikeComment)
bp.route("/deleteComment/<comment_id>",methods=['POST'])(comment_controllers.deleteComment)