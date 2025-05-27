from flask import Blueprint, request, jsonify
from db import bcrypt, SessionLocal
from models import Expense, Category, User
from datetime import datetime
import json


categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validación básica
    required_fields = ['userid', 'categoryname', 'amount', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Verificar si ya existe el usuario
    # with SessionLocal() as session:
    #     if session.query(User).filter_by(email=data['email']).first():
    #         return jsonify({'error': 'El correo ya está registrado'}), 409

    # Hashear la contraseña
    # hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Crear nuevo usuario
    new_category = Category(
        userid=data['userid'],
        categoryname=data['categoryname'],
        icon='1',
    )
    # with Session.begin() as session:
    with SessionLocal() as session:
        session.add(new_category)
        # category = session.query(Category, Category.categoriesid).filter_by(categoryname=data['categoryname'])
        session.commit()
        new_expense = Expense(
            userid=data['userid'],
            categoryid=new_category.categoriesid,
            amount=data['amount'],
            description=data['description'],
        )
        session.add(new_expense)
        session.commit()
        return jsonify({'message': 'Gasto registrado correctamente', 'USERSID': new_expense.expensesid}), 201
    # db.session.add(new_user)
    # db.session.commit()

    

# @expenses_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()

#     # Validación básica
#     required_fields = ['userid', 'categoryid', 'amount', 'description']
#     if not all(field in data for field in required_fields):
#         return jsonify({'error': 'Faltan campos requeridos'}), 400

#     # Verificar si ya existe categoria
#     with SessionLocal() as session:
#         if session.query(Category).filter_by(categoriesid=data['categoryid']).first():
#             return jsonify({'error': 'El correo ya está registrado'}), 409

#     # Hashear la contraseña
#     # hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

#     # Crear nuevo usuario
#     new_expense = Expense(
#         userid=data['userid'],
#         categoryid=data['categoryid'],
#         amount=data['amount'],
#         description=data['description'],  # o usa el ID del admin si estás autenticando
#     )
#     # with Session.begin() as session:
#     with SessionLocal() as session:
#         session.add(new_expense)
#         session.commit()
#     # db.session.add(new_user)
#     # db.session.commit()

#     return jsonify({'message': 'Gasto registrado correctamente', 'USERSID': new_expense.expensesid}), 201

