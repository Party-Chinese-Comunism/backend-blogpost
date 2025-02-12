from app import db
from models.models import Comment

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
