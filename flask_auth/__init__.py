from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.config import Config

# Inicializando extensões
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Importar Blueprints e registrar
    from flask_auth.routes import auth
    app.register_blueprint(auth, url_prefix="/api/auth")

    return app
