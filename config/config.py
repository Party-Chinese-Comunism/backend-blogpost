import os
from dotenv import load_dotenv
from datetime import timedelta

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secreto")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60) # Define o tempo de vida do token de acesso (30 minutos)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7) # Define o tempo de vida do token de refresh (7 dias)
