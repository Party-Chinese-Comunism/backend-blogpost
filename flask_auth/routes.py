from flask import Blueprint, request, jsonify
from flask_auth import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_auth.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Dados incompletos"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email já registrado"}), 400
    
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username já registrado"}), 400

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

    access_token = create_access_token(identity=str(user.id))  # Converte ID para string
    
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()

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

