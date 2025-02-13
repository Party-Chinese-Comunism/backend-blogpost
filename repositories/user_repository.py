from models.models import User, Post, Comment, followers
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


    def get_favorite_posts_by_user(user):
        return user.favorites
        
    @staticmethod
    def follow_user(follower, followed):
        if not UserRepository.is_following(follower, followed):
            follower.following.append(followed)
            db.session.commit()

    @staticmethod
    def unfollow_user(follower, followed):
        if UserRepository.is_following(follower, followed):
            follower.following.remove(followed)
            db.session.commit()

    @staticmethod
    def is_following(follower, followed):
        return follower.following.filter(followers.c.followed_id == followed.id).count() > 0

    @staticmethod
    def get_followers(user):
        return user.followers.all()

    @staticmethod
    def get_following(user):
        return user.following.all()