from app import db
from models.models import Post, favorites

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
    
    @staticmethod
    def is_favorited_by_user(post_id, user_id):
        """ Verifica se o usuário favoritou o post """
        if not user_id:
            return False  # Se o usuário não estiver autenticado, retorna False
        
        return db.session.query(favorites).filter(
            favorites.c.user_id == user_id, 
            favorites.c.post_id == post_id
        ).first() is not None