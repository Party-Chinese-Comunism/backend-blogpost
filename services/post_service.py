import os, socket
from werkzeug.utils import secure_filename
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository
from repositories.user_repository import UserRepository
from utils.file_utils import *
from flask_jwt_extended import get_jwt_identity, jwt_required

UPLOAD_FOLDER = "uploads/"

SERVER_IP = "http://localhost:5000"

class PostService:
    @staticmethod
    def save_post_image(user_id, image):
        """ Salva a imagem do post no servidor """
        if image and allowed_file(image.filename):
            filename = generate_filename(user_id, image.filename)  #  Gera nome único
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            image.save(filepath)
            return f"/uploads/{filename}"  # Retorna o caminho da imagem

        return None

    @staticmethod
    def validate_post_data(data):
        """ Valida se os dados do post estão corretos """
        return "title" in data and "description" in data

    @staticmethod
    def create_post(data, user_id, image=None):
        """ Cria um post com ou sem imagem """
        if not PostService.validate_post_data(data):
            return {"error": "Dados inválidos!"}, 400

        image_url = None
        if image:
            image_url = PostService.save_post_image(user_id, image)  

        new_post = PostRepository.create_post(data["title"], data["description"], user_id, image_url)
        return {
            "id": new_post.id,
            "title": new_post.title,
            "description": new_post.description,
            "user_id": new_post.user_id,
            "image_url": new_post.image_url
        }, 201
    
    @staticmethod
    @jwt_required(optional=True)  # Permite que a requisição seja feita com ou sem autenticação
    def get_all_posts():
        """ Retorna todos os posts formatados para JSON, incluindo autor, imagem do autor, comentários e imagem do post """
        posts = PostRepository.get_all_posts()
        
        # Obtém o ID do usuário autenticado, se existir
        current_user_id = get_jwt_identity()
        
        return [
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "user_id": post.user_id,
                "author": UserRepository.get_username_by_id(post.user_id),
                "author_image": f"{SERVER_IP}/api/user/uploads/profile_pictures/{UserRepository.get_user_profile_image(post.user_id)}" 
                    if UserRepository.get_user_profile_image(post.user_id) else None,  # Retorna a imagem do autor
                "image_url": f"{SERVER_IP}{post.image_url}" if post.image_url else None,  # Retorna a imagem do post
                "favorite_number": post.favorites_count(),
                #  Verifica se o usuário autenticado favoritou esse post
                "favorited_by_user": PostRepository.is_favorited_by_user(post.id, current_user_id) if current_user_id else False,
                "comments_number": comment_count
            }
            for post, comment_count in posts
        ]
    
    @staticmethod
    @jwt_required()
    def get_posts_by_user(user_id):
        """ Retorna todos os posts do usuário logado, incluindo imagem do autor e comentários """
        
        posts = PostRepository.get_posts_by_user(user_id)

        return [
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "user_id": post.user_id,
                "author": UserRepository.get_username_by_id(post.user_id),
                "author_image": f"{SERVER_IP}/api/user/uploads/profile_pictures/{UserRepository.get_user_profile_image(post.user_id)}" 
                    if UserRepository.get_user_profile_image(post.user_id) else None,  # Retorna a imagem do autor
                "image_url": f"{SERVER_IP}{post.image_url}" if post.image_url else None,  # Retorna a imagem do post
            }
            for post in posts
        ]