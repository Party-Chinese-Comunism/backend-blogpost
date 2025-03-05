import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from services.comment_service import CommentService
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository
from repositories.user_repository import UserRepository  # Adicionado para mockar a função get_username_by_id


# Fixture do aplicativo que usa SQLite em memória para os testes
# Vamos evitar o uso do banco real com mocks e não utilizar o banco SQLite
@pytest.fixture
def app():
    app = create_app()
    
    # Defina o banco de dados para SQLite em memória durante os testes
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Não vamos usar banco real nos testes
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # Não precisamos criar e dropar o banco real aqui, porque estamos mockando tudo
        yield app

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
    @patch.object(CommentRepository, 'get_comments_by_post')
    @patch.object(UserRepository, 'get_username_by_id')  # Mockando a função get_username_by_id
    def test_get_comments_by_post(self, mock_get_username_by_id, mock_get_comments_by_post, client):
        post_id = 1
        mock_comment = MagicMock(id=1, content="Comentário", post_id=post_id, user_id=1)
        mock_get_comments_by_post.return_value = [mock_comment]
        mock_get_username_by_id.return_value = "username"  # Retorno mockado para o nome de usuário

        # Simula a chamada para obter os comentários sem interagir com o banco real
        with client.application.test_request_context():  # Cria o contexto de teste
            comments = CommentService.get_comments_by_post(post_id)

        assert len(comments) == 1
        assert comments[0]["content"] == "Comentário"
        assert comments[0]["post_id"] == post_id
        assert comments[0]["user_id"] == 1
        assert comments[0]["username"] == "username"  # Verificando o nome do usuário mockado
"""