from flask import Blueprint, request, jsonify
from db import bcrypt, SessionLocal
from models import User
from datetime import datetime

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['email', 'password', 'name', 'lastname']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    with SessionLocal() as session:
        if session.query(User).filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        new_user = User(
            email=data['email'],
            passwordhash=hashed_password,
            name=data['name'],
            lastname=data['lastname'],
            created=datetime.utcnow(),
            creator=0
        )
        session.add(new_user)
        session.commit()

        return jsonify({'message': 'User registered successfully', 'usersid': new_user.usersid}), 201

@users_bp.route('/getUserById', methods=['POST'])
def get_user_by_id():
    data = request.get_json()
    if not data or 'usersid' not in data:
        return jsonify({'error': 'usersid is required'}), 400

    with SessionLocal() as session:
        user = session.query(User).filter_by(usersid=data['usersid'], isdeleted=False).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'usersid': user.usersid,
        'email': user.email,
        'name': user.name,
        'lastname': user.lastname,
        'created': user.created.isoformat() if user.created else None
    }), 200

@users_bp.route('/getAllUsers', methods=['GET'])
def get_all_users():
    with SessionLocal() as session:
        users = session.query(User).filter_by(isdeleted=False).all()

    result = [{
        'usersid': u.usersid,
        'email': u.email,
        'passwordhash': u.passwordhash,
        'name': u.name,
        'lastname': u.lastname,
        'created': u.created.isoformat() if u.created else None
    } for u in users]

    return jsonify(result), 200

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    with SessionLocal() as session:
        user = session.query(User).filter_by(email=data['email'], isdeleted=False).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not bcrypt.check_password_hash(user.passwordhash, data['password']):
        return jsonify({'error': 'Incorrect password'}), 401

    return jsonify({
        'message': 'Login successful',
        'usersid': user.usersid,
        'email': user.email,
        'name': user.name,
        'lastname': user.lastname
    }), 200
