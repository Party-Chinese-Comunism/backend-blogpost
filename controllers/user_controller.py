import os
from services.user_service import UserService
from repositories.user_repository import UserRepository

from flask import Blueprint, current_app, request, jsonify, send_from_directory, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.file_utils import  SERVER_IP

user_controller = Blueprint('user_controller', __name__)


SERVER_IP = "http://localhost:5000"

@user_controller.route('/upload-profile-image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    """ Upload de imagem para o perfil do usuário autenticado """
    current_user_id = get_jwt_identity()
    image = request.files.get("image")

    if not image:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    updated_user, image_url = UserService.save_profile_image(current_user_id, image)
    
    if not updated_user:
        return jsonify({"error": "Formato de arquivo inválido"}), 400

    return jsonify({
        "message": "Imagem de perfil atualizada com sucesso!",
        "profile_image": f"{SERVER_IP}{image_url}"
    }), 200

@user_controller.route('/profile-image/<int:user_id>', methods=['GET'])
def get_profile_image(user_id):
    """ Retorna a URL da imagem de perfil de um usuário """
    user = UserRepository.get_user_by_id(user_id)
    
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if not user.profile_image:
        return jsonify({"error": "Usuário não tem imagem de perfil"}), 404

    image_url = url_for('user_controller.serve_profile_picture', filename=user.profile_image, _external=True)
    
    return jsonify({"image_url": image_url})

@user_controller.route('/uploads/profile_pictures/<filename>')
def serve_profile_picture(filename):
    """Serve a imagem do diretório de perfil"""
    return send_from_directory(os.path.join(current_app.root_path, "uploads/profile_pictures"), filename)

@user_controller.route('/favorite/<int:post_id>', methods=['POST'])
@jwt_required()
def toogle_favorite(post_id):
    current_user_id = get_jwt_identity()
    
    response, status = UserService.toggle_favorite(current_user_id, post_id)
    return jsonify(response), status

@user_controller.route('/like/<int:comment_id>', methods=['POST'])
@jwt_required()
def toogle_like(comment_id):
    current_user_id = get_jwt_identity()

    response, status = UserService.toggle_like(current_user_id, comment_id)
    return jsonify(response), status

@user_controller.route('/favorites', methods=['GET'])
@jwt_required()
def list_favorites():
    current_user_id = get_jwt_identity()
    
    response, status = UserService.list_favorites(current_user_id)
    return jsonify(response), status

@user_controller.route('/follow/<int:user_id>', methods=['POST'])
@jwt_required()
def toggle_follow(user_id):
    current_user_id = get_jwt_identity()

    response, status = UserService.toggle_follow(current_user_id, user_id)
    return jsonify(response), status

@user_controller.route("/followers", methods=["GET"])
@jwt_required()
def get_followers():  
    current_user_id = get_jwt_identity()

    response, status = UserService.get_followers(current_user_id)
    return jsonify(response), status

@user_controller.route("/following", methods=["GET"])
@jwt_required()
def get_followin():
    current_user_id = get_jwt_identity()
    response, status = UserService.get_following(current_user_id)
    return jsonify(response), status

@user_controller.route("/search-users-by-username/<string:name>", methods=["GET"])
def search_users(name):
    
    response, status = UserService.search_users(name)
    return jsonify(response), status

@user_controller.route("/get-user-by-id/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    
    response, status = UserService.get_user_by_id(user_id)
    return jsonify(response), status
