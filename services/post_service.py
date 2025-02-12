import os
from werkzeug.utils import secure_filename
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository
from repositories.user_repository import UserRepository

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

SERVER_IP = "http://127.0.0.1:5000"

class PostService:
    @staticmethod
    def allowed_file(filename):
        """ Verifica se a extensão da imagem é permitida """
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def save_image(image):
        """ Salva a imagem no servidor e retorna a URL """
        if image and PostService.allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)
            return f"/uploads/{filename}"  # 🔹 URL da imagem salva
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
            image_url = PostService.save_image(image)  # Salva a imagem

        new_post = PostRepository.create_post(data["title"], data["description"], user_id, image_url)
        return {
            "id": new_post.id,
            "title": new_post.title,
            "description": new_post.description,
            "user_id": new_post.user_id,
            "image_url": new_post.image_url
        }, 201
    
    @staticmethod
    def get_all_posts():
        """ Retorna todos os posts formatados para JSON, incluindo autor, comentários e imagem """
        posts = PostRepository.get_all_posts()
        return [
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "user_id": post.user_id,
                "author": UserRepository.get_username_by_id(post.user_id),
                "image_url": f"http://127.0.0.1:5000{post.image_url}" if post.image_url else None,
                "comments": [
                    {
                        "id": comment.id,
                        "content": comment.content,
                        "user_id": comment.user_id,
                        "username": UserRepository.get_username_by_id(comment.user_id),
                        "post_id": comment.post_id
                    }
                    for comment in CommentRepository.get_comments_by_post(post.id)
                ]
            }
            for post in posts
        ]
    
    @staticmethod
    def get_posts_by_user(user_id):
        """ Retorna todos os posts do usuário logado """
        posts = PostRepository.get_posts_by_user(user_id)
        return [
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "user_id": post.user_id,
                "author": UserRepository.get_username_by_id(post.user_id),
                "image_url": f"http://127.0.0.1:5000{post.image_url}" if post.image_url else None,
                "comments": [
                    {
                        "id": comment.id,
                        "content": comment.content,
                        "user_id": comment.user_id,
                        "username": UserRepository.get_username_by_id(comment.user_id),
                        "post_id": comment.post_id
                    }
                    for comment in CommentRepository.get_comments_by_post(post.id)
                ]
            }
            for post in posts
        ]