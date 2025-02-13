from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

favorites = db.Table('favorites', 
    db.Column('user.id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post.id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

likes = db.Table('likes',
    db.Column('user.id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('comment.id', db.Integer, db.ForeignKey('comment.id'), primary_key=True)                 
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_image = db.Column(db.String(256), nullable=True)
    
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)

    favorites = db.relationship('Post', secondary=favorites, backref='favorited_by', lazy=True)
    likes = db.relationship('Comment', secondary=likes, backref='liked_by', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(256), nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), nullable=False)  # JWT ID (identificador único do token)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    jti = db.Column(db.String(120), nullable=False, unique=True)  # Identificador único do token
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 
    revoked = db.Column(db.Boolean, default=False)  # Se o token foi revogado