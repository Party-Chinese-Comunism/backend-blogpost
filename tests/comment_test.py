import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from services.comment_service import CommentService
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository
from repositories.user_repository import UserRepository

# Fixture do aplicativo que usa SQLite em memória para os testes
@pytest.fixture
def app():
    app = create_app()
    
    # Certifique-se de que está usando o banco SQLite em memória
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usando SQLite em memória
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("Banco de dados configurado para SQLite em memória:", app.config['SQLALCHEMY_DATABASE_URI'])

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco em memória
        yield app
        db.session.remove()
        db.drop_all()  # Limpa o banco após os testes

@pytest.fixture
def client(app):
    return app.test_client()  # Retorna um cliente de teste para interagir com a aplicação


class TestCommentService:

    @patch.object(CommentService, 'validate_comment_data')
    @patch.object(PostRepository, 'get_post_by_id')
    @patch.object(CommentRepository, 'create_comment')
    def test_create_comment_invalid_data(self, mock_create_comment, mock_get_post_by_id, mock_validate_comment_data):
        mock_validate_comment_data.return_value = False
        data = {"content": "Test comment", "post_id": 1}
        user_id = 1
    
        response, status_code = CommentService.create_comment(data, user_id)
    
        assert status_code == 400
        assert response["error"] == "Dados inválidos!"
    
    @patch.object(PostRepository, 'get_post_by_id')
    @patch.object(CommentRepository, 'create_comment')
    def test_create_comment_post_not_found(self, mock_create_comment, mock_get_post_by_id):
        data = {"content": "Comentário válido", "post_id": 1}
        user_id = 1
        mock_get_post_by_id.return_value = None  # Simula que o post não existe

        response, status_code = CommentService.create_comment(data, user_id)

        assert status_code == 404
        assert response["error"] == "Post não encontrado!"

    @patch.object(PostRepository, 'get_post_by_id')
    @patch.object(CommentRepository, 'create_comment')
    def test_create_comment_success(self, mock_create_comment, mock_get_post_by_id):
        data = {"content": "Comentário válido", "post_id": 1}
        user_id = 1
        mock_post = MagicMock()  # Mock do post retornado
        mock_get_post_by_id.return_value = mock_post
        mock_create_comment.return_value = MagicMock(id=1, content="Comentário válido", post_id=1, user_id=1)

        response, status_code = CommentService.create_comment(data, user_id)
     
        assert status_code == 201
        assert response["content"] == "Comentário válido"
        assert response["post_id"] == 1
        assert response["user_id"] == 1
"""
tem q arrumar o teste abaixo

    @patch.object(CommentRepository, 'get_comments_by_post')
    @patch.object(UserRepository, 'get_username_by_id')  # Mockando a função get_username_by_id
    @patch('repositories.user_repository.User.query.get')  # Mockando a consulta do User.query.get()
    def test_get_comments_by_post(self, mock_get_user, mock_get_username_by_id, mock_get_comments_by_post, client):
        post_id = 1
        user_id = 1

        # Mockando o usuário retornado
        mock_user = MagicMock()
        mock_user.username = "username"
        mock_get_user.return_value = mock_user

        # Mockando o comentário retornado
        mock_comment = MagicMock(id=1, content="Comentário", post_id=post_id, user_id=user_id)
        mock_get_comments_by_post.return_value = [mock_comment]
        mock_get_username_by_id.return_value = "username"  # Retorno mockado para o nome de usuário

        # Simula a chamada para obter os comentários sem interagir com o banco real
        with client.application.test_request_context():  # Cria o contexto de teste
            comments = CommentService.get_comments_by_post(post_id)

        assert len(comments) == 1
        assert comments[0]["content"] == "Comentário"
        assert comments[0]["post_id"] == post_id
        assert comments[0]["user_id"] == 1
        assert comments[0]["username"] == "username" 
"""
