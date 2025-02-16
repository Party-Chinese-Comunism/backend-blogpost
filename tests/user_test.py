import pytest

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.user_service import UserService
from repositories.user_repository import UserRepository

from unittest.mock import patch, MagicMock


def test_toggle_favorite_add():
    user = MagicMock()
    post = MagicMock()
    user.favorites = []
    
    with patch.object(UserRepository, 'get_user_by_id', return_value=user), \
         patch.object(UserRepository, 'get_post_by_id', return_value=post), \
         patch.object(UserRepository, 'add_favorite') as mock_add_favorite:
        
        response, status_code = UserService.toggle_favorite(1, 1)
        
        mock_add_favorite.assert_called_once_with(user, post)
        assert response == {"message": "Post added to favorite"}
        assert status_code == 200

def test_toggle_favorite_remove():
    user = MagicMock()
    post = MagicMock()
    user.favorites = [post]
    
    with patch.object(UserRepository, 'get_user_by_id', return_value=user), \
         patch.object(UserRepository, 'get_post_by_id', return_value=post), \
         patch.object(UserRepository, 'remove_favorite') as mock_remove_favorite:
        
        response, status_code = UserService.toggle_favorite(1, 1)
        
        mock_remove_favorite.assert_called_once_with(user, post)
        assert response == {"message": "Post remove from favorite. "}
        assert status_code == 200


def test_toggle_like_add():
    user = MagicMock()
    comment = MagicMock()
    user.likes = []
    
    with patch.object(UserRepository, 'get_user_by_id', return_value=user), \
         patch.object(UserRepository, 'get_comment_by_id', return_value=comment), \
         patch.object(UserRepository, 'add_like') as mock_add_like:
        
        response, status_code = UserService.toggle_like(1, 1)
        
        mock_add_like.assert_called_once_with(user, comment)
        assert response == {"message": "Like Added"}
        assert status_code == 200

def test_toggle_follow():
    follower = MagicMock()
    followed = MagicMock()
    
    with patch.object(UserRepository, 'get_user_by_id', side_effect=[follower, followed]), \
         patch.object(UserRepository, 'is_following', return_value=False), \
         patch.object(UserRepository, 'follow_user') as mock_follow:
        
        response, status_code = UserService.toggle_follow(1, 2)
        
        mock_follow.assert_called_once_with(follower, followed)
        assert response == {"message": f"Agora você está seguindo {followed.username}"}
        print (followed.username)
        assert status_code == 200

def test_get_followers():
    user = MagicMock()
    followers = [MagicMock(username='user1'), MagicMock(username='user2')]
    
    with patch.object(UserRepository, 'get_user_by_id', return_value=user), \
         patch.object(UserRepository, 'get_followers', return_value=followers):
        
        response, status_code = UserService.get_followers(1)
        
        assert response == {"followers": ["user1", "user2"]}
        assert status_code == 200

