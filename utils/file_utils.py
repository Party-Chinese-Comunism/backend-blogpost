import time, socket
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
PORT = "5000"
SERVER_IP = f"http://backend:{PORT}"

def allowed_file(filename):
    """ Verifica se o arquivo tem uma extensão permitida """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(user_id, filename):
    """ Gera um nome único para a imagem """
    ext = filename.rsplit(".", 1)[1].lower()  # Obtém a extensão do arquivo
    timestamp = int(time.time())  # Obtém o timestamp atual
    return f"{user_id}-{timestamp}.{ext}"  # Exemplo: 1-123213213123.png

