from app import db
from models.models import Post

class PostRepository:
    @staticmethod
    def create_post(title, description, user_id, image_url=None):
        """ Cria um novo post e salva no banco de dados """
        new_post = Post(title=title, description=description, user_id=user_id, image_url=image_url)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def get_post_by_id(post_id):
        return Post.query.get(post_id)
    
    @staticmethod
    def get_all_posts():
        return Post.query.all()

    @staticmethod
    def get_posts_by_user(user_id):
        """ Obtém todos os posts de um usuário específico """
        return Post.query.filter_by(user_id=user_id).all()