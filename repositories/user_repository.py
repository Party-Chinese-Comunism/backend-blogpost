from models.models import User
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