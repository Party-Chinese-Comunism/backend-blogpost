from models.models import User, Post, Comment
from app import db

class UserRepository:
    @staticmethod
    def get_username_by_id(user_id):
        """ Retorna o nome do usuário com base no ID """
        user = User.query.get(user_id)
        return user.username if user else "Usuário desconhecido"
    
    @staticmethod
    def update_profile_image(user_id, image_url):
        """ Atualiza a imagem do usuário """
        user = User.query.get(user_id)
        if not user:
            return None
        user.profile_image = image_url
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_post_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def get_comment_by_id(comment_id):
        return Comment.query.get(comment_id)

    @staticmethod
    def add_favorite(user, post):
        user.favorites.append(post)
        db.session.commit()

    @staticmethod
    def remove_favorite(user, post):
        user.favorites.remove(post)
        db.session.commit()

    @staticmethod
    def add_like(user, comment):
        user.likes.append(comment)
        db.session.commit()

    @staticmethod
    def remove_like(user, comment):
        user.likes.remove(comment)
        db.session.commit()


