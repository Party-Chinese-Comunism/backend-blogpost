from flask import Flask, send_from_directory
from config.config import ProductionConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from flask_migrate import Migrate
 
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(testing=False):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Limite de 20MB

    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)

    db.init_app(app)
    jwt.init_app(app)
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    migrate.init_app(app, db)

    IMAGE_FOLDER = os.path.join(os.getcwd(), "uploads")

    @app.route('/uploads/<path:filename>')
    def serve_image(filename):
        return send_from_directory(IMAGE_FOLDER, filename)

    from flask_auth.routes import auth
    from controllers.post_controller import post_controller
    from controllers.comment_controller import comment_controller
    from controllers.user_controller import user_controller

    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(post_controller, url_prefix="/api/posts")
    app.register_blueprint(comment_controller, url_prefix="/api/comments")
    app.register_blueprint(user_controller, url_prefix="/api/user")

    return app

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    from models.models import RevokedToken
    jti = jwt_data["jti"]
    return RevokedToken.query.filter_by(jti=jti).first() is not None
