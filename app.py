from flask import Flask, send_from_directory
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from flask_migrate import Migrate

# Inicializando extensões
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as configurações do arquivo config.py

    # Inicializando as extensões
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  # Permitir conexões do frontend
    migrate.init_app(app, db)  # Configura o Flask-Migrate para o banco de dados

    # Configuração de onde as imagens serão armazenadas
    IMAGE_FOLDER = os.path.join(os.getcwd(), "uploads")
 # Rota para servir as imagens # Rota para servir as imagens # Rota para servir as imagens # Rota para servir as imagens
    # Rota para servir as imagens
    @app.route('/uploads/<path:filename>')
    def serve_image(filename):
        return send_from_directory(IMAGE_FOLDER, filename)

    # Importando os blueprints e registrando no aplicativo
    from flask_auth.routes import auth
    from controllers.post_controller import post_controller
    from controllers.comment_controller import comment_controller
    from controllers.user_controller import user_controller
    
    # Registrando os blueprints com o prefixo adequado
    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(post_controller, url_prefix="/api/posts")
    app.register_blueprint(comment_controller, url_prefix="/api/comments")
    app.register_blueprint(user_controller, url_prefix="/api/user")

    return app

# Adicionando a validação da blacklist de tokens
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    from models.models import RevokedToken
    jti = jwt_data["jti"]
    return RevokedToken.query.filter_by(jti=jti).first() is not None
