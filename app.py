from flask import Flask
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Inicializando extensões
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  # Permitir conexões do frontend

    from flask_auth.routes import auth
    app.register_blueprint(auth, url_prefix="/api/auth")

    return app

# 🔹 Adicionando a validação da blacklist de tokens
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    from flask_auth.models import RevokedToken
    jti = jwt_data["jti"]
    return RevokedToken.query.filter_by(jti=jti).first() is not None

