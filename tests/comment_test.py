import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db 
from services.comment_service import CommentService
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository


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
        mock_get_post_by_id.return_value = None 

        response, status_code = CommentService.create_comment(data, user_id)

        assert status_code == 404
        assert response["error"] == "Post não encontrado!"

    @patch.object(PostRepository, 'get_post_by_id')
    @patch.object(CommentRepository, 'create_comment')
    def test_create_comment_success(self, mock_create_comment, mock_get_post_by_id):

        data = {"content": "Comentário válido", "post_id": 1}
        user_id = 1
        mock_post = MagicMock()  
        mock_get_post_by_id.return_value = mock_post
        mock_create_comment.return_value = MagicMock(id=1, content="Comentário válido", post_id=1, user_id=1)

        response, status_code = CommentService.create_comment(data, user_id)

     
        assert status_code == 201
        assert response["content"] == "Comentário válido"
        assert response["post_id"] == 1
        assert response["user_id"] == 1

    @patch.object(CommentRepository, 'get_comments_by_post')
    def test_get_comments_by_post(self, mock_get_comments_by_post, client):
        post_id = 1
        mock_comment = MagicMock(id=1, content="Comentário", post_id=post_id, user_id=1)
        mock_get_comments_by_post.return_value = [mock_comment]

        with client.application.test_request_context(): 
            comments = CommentService.get_comments_by_post(post_id)

        assert len(comments) == 1
        assert comments[0]["content"] == "Comentário"
        assert comments[0]["post_id"] == post_id
        assert comments[0]["user_id"] == 1
