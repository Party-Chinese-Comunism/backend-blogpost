import os
from werkzeug.utils import secure_filename
from repositories.user_repository import UserRepository

UPLOAD_FOLDER = "uploads/profile_pictures/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

class UserService:
    @staticmethod
    def allowed_file(filename):
        """ Verifica se a extensão da imagem é permitida """
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def save_profile_image(user_id, image):
        """ Salva a imagem no servidor e atualiza o perfil do usuário """
        if image and UserService.allowed_file(image.filename):
            filename = secure_filename(f"user_{user_id}.{image.filename.rsplit('.', 1)[1].lower()}")  # Nome único
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)  # Criar diretório se não existir

            image.save(filepath)
            image_url = f"/uploads/profile_pictures/{filename}"

            updated_user = UserRepository.update_profile_image(user_id, image_url)
            return updated_user, image_url

        return None, None