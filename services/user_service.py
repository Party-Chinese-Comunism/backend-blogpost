from repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def toggle_favorite(user_id, post_id):
        user = UserRepository.get_user_by_id(user_id)
        post = UserRepository.get_post_by_id(post_id)
        print(user.username)
        if not user or not post:
            return {"error": "User or Post not find"}, 400
        
        if post in user.favorites:
            UserRepository.remove_favorite(user, post)
            return {"message": f"Post '{post.title}' remove from favorite. "}, 200
        
        UserRepository.add_favorite(user, post)
        
        return {"message": f"Post '{post.title}' added to favorite"}, 200