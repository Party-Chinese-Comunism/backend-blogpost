from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.comment_service import CommentService

comment_controller = Blueprint('comment_controller', __name__)

@comment_controller.route('/create', methods=['POST'])
@jwt_required()  #  Apenas usuários logados podem comentar
def create_comment():
    """ Apenas usuários logados podem comentar em um post """
    data = request.get_json()
    current_user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado

    response, status = CommentService.create_comment(data, current_user_id)
    return jsonify(response), status

@comment_controller.route('/list/<int:post_id>', methods=['GET'])
def list_comments(post_id):
    """ Retorna todos os comentários de um post """
    comments = CommentService.get_comments_by_post(post_id)
    return jsonify(comments), 200
