from app import db
from models.models import Comment, likes

class CommentRepository:
    @staticmethod
    def create_comment(content, post_id, user_id):
        """ Cria um novo comentário para um post específico """
        new_comment = Comment(content=content, post_id=post_id, user_id=user_id)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment
    
    @staticmethod
    def get_comments_by_post(post_id):
        """ Obtém todos os comentários de um post específico """
        return Comment.query.filter_by(post_id=post_id).all()

    @staticmethod
    def user_liked_comment(comment_id, user_id):
        """ Verifica se um usuário curtiu um comentário """
        if not user_id:
            return False  # Se o usuário não estiver autenticado, retorna False

        # Corrigindo a consulta para usar filter() ao invés de filter_by()
        return db.session.query(likes).filter(
            likes.c.user_id == user_id,  # Correta referência à coluna user_id
            likes.c.comment_id == comment_id  # Correta referência à coluna comment_id
        ).first() is not None