from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.post_service import PostService

post_controller = Blueprint('post_controller', __name__)

@post_controller.route('/create', methods=['POST'])
@jwt_required()  # Apenas usuários logados podem postar
def create_post():
    """ Criação de post com ou sem imagem """
    data = request.form  # Captura os dados do formulário
    image = request.files.get("image")  # Captura a imagem, se houver
    current_user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado

    response, status = PostService.create_post(data, current_user_id, image)
    return jsonify(response), status

@post_controller.route('/list', methods=['GET'])
def list_posts():
    """ Retorna todos os posts cadastrados """
    posts = PostService.get_all_posts()
    return jsonify(posts), 200