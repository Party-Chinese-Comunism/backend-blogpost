from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
)
from models.models import User, RevokedToken, RefreshToken

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Dados incompletos"}), 422

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email já registrado"}), 409
    
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username já registrado"}), 409

    new_user = User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Dados incompletos"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Credenciais inválidas"}), 401

    # Correção: Criando os tokens corretamente
    access_token = create_access_token(identity=str(user.id))  # Access Token (30 min)
    refresh_token = create_refresh_token(identity=str(user.id))  # Refresh Token (7 dias)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200

@auth.route('/logout', methods=['POST'])
@jwt_required(refresh=True)  # Exige um Refresh Token válido
def logout():
    """ Revoga o Refresh Token ao sair """
    jti = get_jwt()["jti"]  # Obtém o identificador único do token
    stored_token = RefreshToken.query.filter_by(jti=jti).first()

    if stored_token:
        stored_token.revoked = True  # Revoga o token
        db.session.commit()

    return jsonify({"message": "Logout realizado com sucesso!"}), 200


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """ Gera um novo token de acesso usando o Refresh Token """
    current_user_id = get_jwt_identity()
    jti = get_jwt()["jti"]  # Obtém o identificador único do token

    # Verifica se o Refresh Token está no banco e não foi revogado
    stored_token = RefreshToken.query.filter_by(jti=jti, user_id=current_user_id).first()

    if not stored_token or stored_token.revoked:
        return jsonify({"error": "Token de refresh inválido ou revogado"}), 401

    # Gera um novo Access Token
    new_access_token = create_access_token(identity=current_user_id)

    return jsonify({"access_token": new_access_token}), 200

# Rota apenas para teste do JWT
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    
    # Verifica se o token foi revogado manualmente
    jti = get_jwt()["jti"]
    if RevokedToken.query.filter_by(jti=jti).first():
        return jsonify({"error": "Token revogado. Faça login novamente."}), 401

    try:
        user = User.query.get(int(current_user_id))  # Converte o ID para inteiro
    except ValueError:
        return jsonify({"error": "Token inválido"}), 400  # Caso o token não contenha um ID válido

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200

  
  #METODO SEGUIR E DEIXAR DE SEGUIR #
@auth.route('/api/user/follow/<int:user_id>', methods=['POST'])
@jwt_required()  
def follow_user(user_id):
    current_user_id = get_jwt_identity()  
    current_user = User.query.get(current_user_id)  
    user_to_follow = User.query.get(user_id)  

    if not user_to_follow:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if current_user.id == user_to_follow.id:
        return jsonify({"error": "Você não pode seguir a si mesmo"}), 400

    # Segue o usuario
    current_user.follow(user_to_follow)
    db.session.commit()

    return jsonify({"message": f"Você está seguindo {user_to_follow.username}"}), 200

@auth.route('/api/user/unfollow/<int:user_id>', methods=['POST'])
@jwt_required() 
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()  
    current_user = User.query.get(current_user_id)  
    user_to_unfollow = User.query.get(user_id)  

    if not user_to_unfollow:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Deixa de seguir o usuario
    current_user.unfollow(user_to_unfollow)
    db.session.commit()

    return jsonify({"message": f"Você deixou de seguir {user_to_unfollow.username}"}), 200
