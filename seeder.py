from app import create_app, db  # Importando a função que cria o app e o db
from models.models import User, Post, Comment  # Ajuste para importar os modelos
from faker import Faker
import random

app = create_app()  # Supondo que você tenha uma função para criar o app
fake = Faker()

def create_fake_users(n):
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password_hash=fake.password(),
            profile_image=fake.image_url()
        )
        db.session.add(user)
    db.session.commit()

def create_fake_posts(n):
    users = User.query.all()
    for _ in range(n):
        post = Post(
            title = fake.sentence()[:20],
            description = fake.paragraph()[:255],
            user_id=random.choice(users).id,
            image_url=fake.image_url(),
        )
        db.session.add(post)
    db.session.commit()

def create_fake_comments(n):
    posts = Post.query.all()
    users = User.query.all()
    for _ in range(n):
        comment = Comment(
            content=fake.text(),
            user_id=random.choice(users).id,
            post_id=random.choice(posts).id
        )
        db.session.add(comment)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():  # Criando o contexto do app Flask
        create_fake_users(10)
        create_fake_posts(20)
        create_fake_comments(50)
