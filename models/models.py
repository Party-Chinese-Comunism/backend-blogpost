from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Tabelas de associação (nomes no plural)
favorites = db.Table('favorites',
    db.Column('user_id', db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.BigInteger, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
)

likes = db.Table('likes',
    db.Column('user_id', db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('comment_id', db.BigInteger, db.ForeignKey('comments.id', ondelete='CASCADE'), primary_key=True)                 
)

followers = db.Table('followers',
    db.Column('follower_id', db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('followed_id', db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
)

# Modelo Users (singular para classe, plural para tabela)
class User(db.Model):
    __tablename__ = 'users'  # Nome da tabela no plural
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_image = db.Column(db.String(256), nullable=True)

    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete")
    comments = db.relationship('Comment', backref='commenter', lazy=True, cascade="all, delete")

    favorites = db.relationship('Post', secondary=favorites, backref=db.backref('favorited_by', lazy='dynamic'))
    likes = db.relationship('Comment', secondary=likes, backref=db.backref('liked_by', lazy='dynamic'))

    following = db.relationship(
        'User',  # Auto-referência
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo Post (singular para classe)
class Post(db.Model):
    __tablename__ = 'posts'  # Nome da tabela no plural
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    update_at = db.Column(db.DateTime, server_default=db.func.now())  # Trigger substitui server_onupdate

    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete")

    def favorites_count(self):
        return self.favorited_by.count()

# Modelo Comment (singular para classe)
class Comment(db.Model):
    __tablename__ = 'comments'  # Nome da tabela no plural
    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.BigInteger, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    def likes_count(self):
        return self.liked_by.count()

# Modelo RevokedToken (singular para classe)
class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'  # Nome da tabela no plural
    id = db.Column(db.BigInteger, primary_key=True)
    jti = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Modelo RefreshToken (singular para classe)
class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'  # Nome da tabela no plural
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    jti = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    revoked = db.Column(db.Boolean, default=False)