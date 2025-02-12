from app import db
from models.models import User, Post

class UserRepository:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_post_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def add_favorite(user, post):
        user.favorites.append(post)
        db.session.commit()

    @staticmethod
    def remove_favorite(user, post):
        user.favorites.remove(post)
        db.session.commit()

