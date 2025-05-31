from flask import Blueprint, request, jsonify
from db import bcrypt, SessionLocal
from models import Expense, Category, User
from datetime import datetime
import json


expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/getAllExpenses', methods=['POST'])
def get_all_expenses():
    #users = User.query.filter_by(ISDELETED=False).all()
    # result = []
    # data = request.get_json()
    # request_data = request.data
    # request_data = json.loads(request_data.decode('utf-8'))
    usersid = int(request.json['usersid'])
    print(usersid)
    print(type(usersid))
    # if not data or 'usersid' not in data:
    #     return jsonify({'error': 'Debe proporcionar el USERSID'}), 400

    with SessionLocal() as session:
        expenses = session.query(Expense.amount, Category.categoryname, Expense.description).\
        join(Category, Expense.categoryid==Category.categoriesid).join(User, Expense.userid==User.usersid).where(User.usersid==usersid).all()
        # result.append((a, b, c))


    result = []
    # for expense in expenses:
    #     result.append({
    #         'amount': expenses.amount,
    #         'categoryname': expenses.categoryname,
    #         'description': expenses.description,
    #     })
    for expense in expenses:
        result.append({
            'amount': expense.amount,
            'categoryname': expense.categoryname,
            'description': expense.description,
        })

    return jsonify(result), 200
@expenses_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validación básica
    required_fields = ['userid', 'categoryid', 'amount', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Crear nuevo usuario
    new_expense = Expense(
        userid=data['userid'],
        categoryid=data['categoryid'],
        amount=data['amount'],
        description=data['description'],  # o usa el ID del admin si estás autenticando
    )
    # with Session.begin() as session:
    with SessionLocal() as session:
        session.add(new_expense)
        session.commit()
    # db.session.add(new_user)
    # db.session.commit()

    return jsonify({'message': 'Gasto registrado correctamente', 'USERSID': new_expense.expensesid}), 201

