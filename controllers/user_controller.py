from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import UserService

user_controller = Blueprint('user_controlller', __name__)

@user_controller.route('/favorite/<int:post_id>', methods=['POST'])
@jwt_required()
def toogle_favorite(post_id):
    current_user_id = get_jwt_identity()
    
    response, status = UserService.toggle_favorite(current_user_id, post_id)
    return jsonify(response), status