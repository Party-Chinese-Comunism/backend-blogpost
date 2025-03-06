import socket
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.post_service import PostService
from repositories.post_repository import PostRepository
from utils.file_utils import  SERVER_IP

post_controller = Blueprint('post_controller', __name__)


SERVER_IP = "http://localhost:5000"

@post_controller.route('/create', methods=['POST'])
@jwt_required() 
def create_post():
    """ Criação de post com ou sem imagem """
    data = request.form  
    image = request.files.get("image")  
    current_user_id = get_jwt_identity()

    response, status = PostService.create_post(data, current_user_id, image)
    return jsonify(response), status

@post_controller.route('/list', methods=['GET'])
def list_posts():
    """ Retorna todos os posts cadastrados """
    posts = PostService.get_all_posts()
    return jsonify(posts), 200

@post_controller.route('/my-posts', methods=['GET'])
@jwt_required()  # Apenas usuários logados podem acessar
def list_my_posts():
    """ Retorna todos os posts do usuário logado """
    current_user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
    posts = PostService.get_posts_by_user(current_user_id)
    return jsonify(posts), 200

@post_controller.route('/<int:user_id>', methods=['GET'])
def posts_by_user(user_id):
    """ Retorna todos os posts de um usuário """
    posts = PostService.get_posts_by_user(user_id)
    return jsonify(posts), 200

@post_controller.route('/upload-post-image', methods=['POST'])
@jwt_required()
def upload_post_image():
    """ Upload de imagem para um post """
    current_user_id = get_jwt_identity()
    image = request.files.get("image")

    if not image:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    image_url = PostService.save_post_image(current_user_id, image)

    if not image_url:
        return jsonify({"error": "Formato de arquivo inválido"}), 400

    return jsonify({
        "message": "Imagem do post enviada com sucesso!",
        "image_url": f"{SERVER_IP}/uploads/{image_url}"
    }), 200