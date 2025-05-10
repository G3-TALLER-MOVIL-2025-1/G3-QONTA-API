from flask import Blueprint, request, jsonify
from db import db, bcrypt
from models import User
from datetime import datetime


users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validación básica
    required_fields = ['EMAIL', 'PASSWORD', 'NAME', 'LASTNAME']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Verificar si ya existe el usuario
    if User.query.filter_by(EMAIL=data['EMAIL']).first():
        return jsonify({'error': 'El correo ya está registrado'}), 409

    # Hashear la contraseña
    hashed_pw = bcrypt.generate_password_hash(data['PASSWORD']).decode('utf-8')

    # Crear nuevo usuario
    new_user = User(
        EMAIL=data['EMAIL'],
        PASSWORDHASH=hashed_pw,
        NAME=data['NAME'],
        LASTNAME=data['LASTNAME'],
        CREATED=datetime.utcnow(),
        CREATOR=0  # o usa el ID del admin si estás autenticando
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado correctamente', 'USERSID': new_user.USERSID}), 201

@users_bp.route('/getUserById', methods=['POST'])
def get_user_by_id():
    data = request.get_json()
    if not data or 'USERSID' not in data:
        return jsonify({'error': 'Debe proporcionar el USERSID'}), 400

    user = User.query.filter_by(USERSID=data['USERSID'], ISDELETED=False).first()

    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({
        'USERSID': user.USERSID,
        'EMAIL': user.EMAIL,
        'NAME': user.NAME,
        'LASTNAME': user.LASTNAME,
        'CREATED': user.CREATED.isoformat() if user.CREATED else None
    }), 200

@users_bp.route('/getAllUsers', methods=['GET'])
def get_all_users():
    users = User.query.filter_by(ISDELETED=False).all()

    result = []
    for user in users:
        result.append({
            'USERSID': user.USERSID,
            'EMAIL': user.EMAIL,
            'NAME': user.NAME,
            'LASTNAME': user.LASTNAME,
            'CREATED': user.CREATED.isoformat() if user.CREATED else None
        })

    return jsonify(result), 200

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    if not data or 'EMAIL' not in data or 'PASSWORD' not in data:
        return jsonify({'error': 'Se requiere EMAIL y PASSWORD'}), 400

    user = User.query.filter_by(EMAIL=data['EMAIL'], ISDELETED=False).first()

    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    if not bcrypt.check_password_hash(user.PASSWORDHASH, data['PASSWORD']):
        return jsonify({'error': 'Contraseña incorrecta'}), 401

    return jsonify({
        'message': 'Login exitoso',
        'USERSID': user.USERSID,
        'EMAIL': user.EMAIL,
        'NAME': user.NAME,
        'LASTNAME': user.LASTNAME
    }), 200
