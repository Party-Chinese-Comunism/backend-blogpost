from flask import Flask, send_from_directory, request
from config.config import ProductionConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate, init, migrate as run_migrate, stamp, upgrade
import os

# Extensões globais
db = SQLAlchemy()
jwt = JWTManager()
migrator = Migrate()

def run_migrations(app, autogenerate=True):
    """Executa as migrations automaticamente ao iniciar."""
    with app.app_context():
        migrations_folder = os.path.join(os.getcwd(), "migrations")
        versions_folder = os.path.join(migrations_folder, "versions")

        if not os.path.exists(migrations_folder):
            print("[INFO] Diretório de migrations não existe. Inicializando alembic...")
            init()
            stamp()
        elif not os.path.exists(versions_folder) or not os.listdir(versions_folder):
            print("[INFO] Diretório de versions vazio. Aplicando stamp...")
            stamp()

        if autogenerate:
            print("[INFO] Gerando novas migrations (se necessário)...")
            try:
                run_migrate(message="Automated migration")
            except Exception as e:
                print(f"[WARNING] Falha ao gerar migrations: {e}")

        print("[INFO] Aplicando migrations ao banco de dados...")
        try:
            upgrade()
            print("[INFO] Migrations aplicadas com sucesso!")
        except Exception as e:
            print(f"[ERROR] Falha ao aplicar migrations: {e}")
            exit(1)

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
    migrator.init_app(app, db)

    CORS(
        app,
        origins=r".*",
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )


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

    # Executar migrations automaticamente
    run_migrations(app, autogenerate=not testing)

    return app

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    from models.models import RevokedToken
    jti = jwt_data["jti"]
    return RevokedToken.query.filter_by(jti=jti).first() is not None
