from flask import Blueprint, request, jsonify
from db import bcrypt, SessionLocal
from models import User
from datetime import datetime


users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validación básica
    required_fields = ['email', 'password', 'name', 'lastname']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Verificar si ya existe el usuario
    with SessionLocal() as session:
        if session.query(User).filter_by(email=data['email']).first():
            return jsonify({'error': 'El correo ya está registrado'}), 409
        else:
            # hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            new_user = User(
                email=data['email'],
                # passwordhash=hashed_pw,
                passwordhash=data['password'],
                name=data['name'],
                lastname=data['lastname'],
                created=datetime.utcnow(),
                creator=0  # o usa el ID del admin si estás autenticando
            )
            session.add(new_user)
            session.commit()
            return jsonify({'message': 'Usuario registrado correctamente', 'USERSID': new_user.usersid}), 201
    # Hashear la contraseña
    # hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # # Crear nuevo usuario
    # new_user = User(
    #     email=data['email'],
    #     passwordhash=hashed_pw,
    #     name=data['name'],
    #     lastname=data['lastname'],
    #     created=datetime.utcnow(),
    #     creator=0  # o usa el ID del admin si estás autenticando
    # )
    # print(new_user.usersid)
    # # with Session.begin() as session:
    # with SessionLocal() as session:
    #     session.add(new_user)
    #     session.commit()
    # # db.session.add(new_user)
    # # db.session.commit()

    # return jsonify({'message': 'Usuario registrado correctamente', 'USERSID': new_user.email}), 201

@users_bp.route('/getUserById', methods=['POST'])
def get_user_by_id():
    data = request.get_json()
    if not data or 'usersid' not in data:
        return jsonify({'error': 'Debe proporcionar el USERSID'}), 400

    with SessionLocal() as session:
        user = session.query(User).filter_by(usersid=data['usersid'], isdeleted=False).first()

    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify([{
        'usersid': user.usersid,
        'email': user.email,
        'name': user.name,
        'lastname': user.lastname,
        'created': user.created.isoformat() if user.created else None
    }]), 200

@users_bp.route('/getAllUsers', methods=['GET'])
def get_all_users():
    with SessionLocal() as session:
        users = session.query(User).filter_by(isdeleted=False).all()
        # users = session.query(User).filter_by(isdeleted=False).all()
    

    result = []
    for user in users:

        result.append({
            'usersid': user.usersid,
            'email': user.email,
            'passwordhash': user.passwordhash,
            'name': user.name,
            'lastname': user.lastname,
            'created': user.created.isoformat() if user.created else None
        })

    return jsonify(result), 200

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Se requiere EMAIL y PASSWORD'}), 400
    
    with SessionLocal() as session:
        user = session.query(User).filter_by(email=data['email'], ISDELETED=False).first()

    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    if not bcrypt.check_password_hash(user.passwordhash, data['password']):
        return jsonify({'error': 'Contraseña incorrecta'}), 401

    return jsonify({
        'message': 'Login exitoso',
        'usersid': user.usersid,
        'email': user.email,
        'name': user.name,
        'lastname': user.lastname
    }), 200
