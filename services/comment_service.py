from repositories.comment_repository import CommentRepository
from repositories.post_repository import PostRepository
from flask_jwt_extended import get_jwt_identity, jwt_required

class CommentService:
    @staticmethod
    def validate_comment_data(data):
        """ Valida se os dados do comentário estão corretos """
        return data and "content" in data and "post_id" in data

    @staticmethod
    def create_comment(data, user_id):
        """ Valida e cria um comentário em um post """
        if not CommentService.validate_comment_data(data):
            return {"error": "Dados inválidos!"}, 400

        post_id = data.get("post_id")
        post = PostRepository.get_post_by_id(post_id)

        if not post:
            return {"error": "Post não encontrado!"}, 404
        
        new_comment = CommentRepository.create_comment(data["content"], post_id, user_id)
        
        return {
            "id": new_comment.id,
            "content": new_comment.content,
            "post_id": new_comment.post_id,
            "user_id": new_comment.user_id
        }, 201

    @staticmethod
    @jwt_required(optional=True)
    def get_comments_by_post(post_id):

        current_user_id = get_jwt_identity()

        """ Retorna todos os comentários de um post específico """
        comments = CommentRepository.get_comments_by_post(post_id)
        
        return [
            {
                "id": comment.id,
                "content": comment.content,
                "post_id": comment.post_id,
                "user_id": comment.user_id,
                "like_number": comment.likes_count(),
                "liked_by_user": CommentRepository.user_liked_comment(comment.id, current_user_id) if current_user_id else False
            }
            for comment in comments
        ]
