import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db  
from services.post_service import PostService 
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from werkzeug.datastructures import FileStorage

# Fixture do aplicativo que usa SQLite em memória para os testes
@pytest.fixture
def app():
    app = create_app()

    # Confirmação de que o banco de dados é SQLite em memória
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Configuração para usar o SQLite em memória
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usando SQLite em memória
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco em memória
        yield app
        db.session.remove()
        db.drop_all()  # Limpa o banco após os testes


@pytest.fixture
def client(app):
    return app.test_client()  # Retorna um cliente de teste para interagir com a aplicação

def test_create_post_without_image(app):
    data = {"title": "Test Post", "description": "This is a test post."}
    user_id = 1
    
    with app.app_context():   
        with patch.object(PostRepository, 'create_post') as mock_create_post:
            mock_create_post.return_value = MagicMock(
                id=1, title="Test Post", description="This is a test post.", user_id=user_id, image_url=None
            )

            response, status_code = PostService.create_post(data, user_id)
            
            mock_create_post.assert_called_once_with("Test Post", "This is a test post.", user_id, None)
            assert response["title"] == "Test Post"
            assert response["description"] == "This is a test post."
            assert status_code == 201

def test_create_post_with_image(app):
    data = {"title": "Test Post with Image", "description": "This post has an image."}
    user_id = 1
    
    mock_image = MagicMock(spec=FileStorage)
    mock_image.filename = "test_image.jpg"
    
    with app.app_context():
        with patch.object(PostRepository, 'create_post') as mock_create_post, \
             patch.object(PostService, 'save_post_image', return_value="/uploads/test_image.jpg"):
            
            mock_create_post.return_value = MagicMock(
                id=1, title="Test Post with Image", description="This post has an image.", user_id=user_id, image_url="/uploads/test_image.jpg"
            )
            
            response, status_code = PostService.create_post(data, user_id, image=mock_image)
            
            mock_create_post.assert_called_once_with("Test Post with Image", "This post has an image.", user_id, "/uploads/test_image.jpg")
            assert response["title"] == "Test Post with Image"
            assert response["description"] == "This post has an image."
            assert response["image_url"] == "/uploads/test_image.jpg"
            assert status_code == 201

def test_create_post_invalid_data():
    data = {"title": "", "description": ""}
    user_id = 1 

    if not data.get("title") or not data.get("description"):
        return {"error": "Dados inválidos!"}, 400

    with patch.object(PostRepository, 'create_post') as mock_create_post:
        response, status_code = PostService.create_post(data, user_id)

        # Verificando que a criação de post não foi chamada, pois os dados são inválidos
        assert mock_create_post.call_count == 0  

def test_save_post_image(app):
    user_id = 1
    mock_image = MagicMock(spec=FileStorage)
    mock_image.filename = "test_image.jpg"
    
    with app.app_context():
        with patch("os.makedirs") as mock_makedirs, patch("werkzeug.utils.secure_filename") as mock_secure_filename:
            mock_secure_filename.return_value = "test_image.jpg"
            
            upload_folder = "uploads/"
           # os.makedirs(upload_folder, exist_ok=True)
            
            image_url = PostService.save_post_image(user_id, mock_image)
            
            assert image_url.startswith("/uploads/1-") 
            assert image_url.endswith(".jpg")
            mock_makedirs.assert_called_once_with("uploads/", exist_ok=True)
