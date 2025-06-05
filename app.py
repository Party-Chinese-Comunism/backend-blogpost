from flask import Flask, send_from_directory
from config.config import ProductionConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate, upgrade, init, migrate, stamp
import os

# Extensões globais
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def run_migrations(app):
    """Executa as migrations automaticamente ao iniciar."""
    with app.app_context():
        migrations_folder = os.path.join(os.getcwd(), "migrations")

        if not os.path.exists(migrations_folder):
            print("[INFO] Criando diretório de migrations automaticamente...")
            init()
            stamp() 

        print("[INFO] Gerando novas migrations (se necessário)...")
        migrate(message="Automated migration")

        print("[INFO] Aplicando migrations ao banco de dados...")
        upgrade()
        print("[INFO] Migrations aplicadas com sucesso!")

def run_tests():
    """Executa os testes automatizados com SQLite."""
    import pytest
    test_app = create_app(testing=True)
    with test_app.app_context():
        from app import db
        db.create_all()
    print("[INFO] Executando testes automatizados...")
    pytest.main(["-q", "--disable-warnings", "tests/"])

def create_app(testing=False):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    CORS(app,
        origins=lambda: request.headers.get("Origin"),
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Servir imagens da pasta uploads
    IMAGE_FOLDER = os.path.join(os.getcwd(), "uploads")

    @app.route('/uploads/<path:filename>')
    def serve_image(filename):
        return send_from_directory(IMAGE_FOLDER, filename)

    # Registro de rotas (blueprints)
    from flask_auth.routes import auth
    from controllers.post_controller import post_controller
    from controllers.comment_controller import comment_controller
    from controllers.user_controller import user_controller

    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(post_controller, url_prefix="/api/posts")
    app.register_blueprint(comment_controller, url_prefix="/api/comments")
    app.register_blueprint(user_controller, url_prefix="/api/user")

    run_migrations(app)

    return app

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    from models.models import RevokedToken
    jti = jwt_data["jti"]
    return RevokedToken.query.filter_by(jti=jti).first() is not None
