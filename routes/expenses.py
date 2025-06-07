from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import Expense, Category, User
from datetime import datetime

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/getAllExpenses', methods=['POST'])
def getAllExpenses():
    data = request.get_json()

    if not data or 'usersid' not in data:
        return jsonify({'error': 'Debe proporcionar el usersid'}), 400

    usersid = int(data['usersid'])

    with SessionLocal() as session:
        expenses = session.query(
            Expense.amount,
            Category.categoryname,
            Expense.description
        ).join(Category, Expense.categoryid == Category.categoriesid
        ).join(User, Expense.userid == User.usersid
        ).filter(User.usersid == usersid).all()

        result = [{
            'amount': expense.amount,
            'categoryName': expense.categoryname,
            'description': expense.description
        } for expense in expenses]

    return jsonify(result), 200

@expenses_bp.route('/register', methods=['POST'])
def registerExpense():
    data = request.get_json()

    required_fields = ['userid', 'categoryid', 'amount', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    new_expense = Expense(
        userid=data['userid'],
        categoryid=data['categoryid'],
        amount=data['amount'],
        description=data['description'],
        created=datetime.utcnow(),
        creator=data['userid']
    )

    with SessionLocal() as session:
        session.add(new_expense)
        session.flush()  # Genera expensesid
        expenseId = new_expense.expensesid
        session.commit()

    return jsonify({
        'message': 'Gasto registrado correctamente',
        'expenseId': expenseId
    }), 201
