import os
from werkzeug.utils import secure_filename
from repositories.user_repository import UserRepository
from utils.file_utils import allowed_file, generate_filename

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

class UserService:
    @staticmethod
    def allowed_file(filename):
        """ Verifica se a extensão da imagem é permitida """
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def save_profile_image(user_id, image):
        """ Salva a imagem no servidor e atualiza o perfil do usuário """
        if image and allowed_file(image.filename):
            filename = generate_filename(user_id, image.filename)  # 🔹 Gera nome único
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            image.save(filepath)  # 🔹 Salva a imagem no diretório
            image_url = f"/uploads/profile_pictures/{filename}"

            updated_user = UserRepository.update_profile_image(user_id, image_url)
            return updated_user, image_url

        return None, None

    @staticmethod
    def toggle_favorite(user_id, post_id):
        user = UserRepository.get_user_by_id(user_id)
        post = UserRepository.get_post_by_id(post_id)
        print(user.username)
        if not user or not post:
            return {"error": "User or Post not find"}, 400
        
        if post in user.favorites:
            UserRepository.remove_favorite(user, post)
            return {"message": f"Post '{post.title}' remove from favorite. "}, 200
        
        UserRepository.add_favorite(user, post)
        
        return {"message": f"Post '{post.title}' added to favorite"}, 200