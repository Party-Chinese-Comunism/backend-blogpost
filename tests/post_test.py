import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db  # Importando corretamente o Flask app
from services.post_service import PostService 
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from werkzeug.datastructures import FileStorage

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# Teste para criação de post sem imagem
def test_create_post_without_image(app):
    data = {"title": "Test Post", "description": "This is a test post."}
    user_id = 1
    
    with app.app_context():  # Garante que o teste roda dentro do contexto do Flask
        with patch.object(PostRepository, 'create_post') as mock_create_post:
            mock_create_post.return_value = MagicMock(
                id=1, title="Test Post", description="This is a test post.", user_id=user_id, image_url=None
            )

            response, status_code = PostService.create_post(data, user_id)
            
            mock_create_post.assert_called_once_with("Test Post", "This is a test post.", user_id, None)
            assert response["title"] == "Test Post"
            assert response["description"] == "This is a test post."
            assert status_code == 201

# Teste para criação de post com imagem
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

#ajustar (validate_post_data) na service 
def test_create_post_invalid_data():
    data = {"title": "", "description": ""}
    user_id = 1

    with patch.object(PostRepository, 'create_post') as mock_create_post:
        response, status_code = PostService.create_post(data, user_id)

        
        assert mock_create_post.call_count == 0  



def test_save_post_image(app):
    user_id = 1
    mock_image = MagicMock(spec=FileStorage)
    mock_image.filename = "test_image.jpg"
    
    with app.app_context():
        with patch("os.makedirs") as mock_makedirs, patch("werkzeug.utils.secure_filename") as mock_secure_filename:
            mock_secure_filename.return_value = "test_image.jpg"
            
            image_url = PostService.save_post_image(user_id, mock_image)
            
            assert image_url.startswith("/uploads/1-")  # O nome pode mudar pelo timestamp
            assert image_url.endswith(".jpg")
            mock_makedirs.assert_called_once_with("uploads/", exist_ok=True)
