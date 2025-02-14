
from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import UserService
from repositories.user_repository import UserRepository
import os
from flask import Blueprint, jsonify
 

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
    user = UserRepository.get_username_by_id(user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    image_path = os.path.join("uploads/", f"user_{user_id}.jpg")
    if not os.path.exists(image_path):
        return jsonify({"error": "Imagem não encontrada"}), 404

    return send_from_directory(os.path.abspath("uploads/"), f"user_{user_id}.jpg")

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