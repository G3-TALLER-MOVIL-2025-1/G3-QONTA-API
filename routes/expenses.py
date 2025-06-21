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

@expenses_bp.route('/getProfileData', methods=['POST'])
def get_profile_data():
    data = request.get_json()
    if not data or 'usersid' not in data:
        return jsonify({'error': 'Debe proporcionar el USERSID'}), 400

    with SessionLocal() as session:
        user = session.query(User).filter_by(usersid=data['usersid'], isdeleted=False).first()
        if not user:
            return jsonify({'error': 'Usuario no encontrado o eliminado'}), 404

        expenses = session.query(Expense).filter_by(userid=data['usersid'], isdeleted=False).order_by(Expense.created.desc()).all()

    if not expenses:
        return jsonify({
            'email': user.email,
            'fullname': f'{user.name} {user.lastname}',
            'amount': 0,
            'date': None,
            'message': 'No se encontraron gastos para este usuario'
        }), 200

    last_expense = expenses[0]
    return jsonify([{
        'email': user.email,
        'fullname': f'{user.name} {user.lastname}',
        'amount': last_expense.amount,
        'date': str(last_expense.created)[:10],
    }]), 200

@expenses_bp.route('/getExpenseById', methods=['POST'])
def get_expense_by_id():
    data = request.get_json()
    if not data or 'expenseId' not in data:
        return jsonify({'error': 'Debe proporcionar el expenseId'}), 400

    expense_id = int(data['expenseId'])

    with SessionLocal() as session:
        expense = session.query(Expense).filter_by(expensesid=expense_id, isdeleted=False).first()
        if not expense:
            return jsonify({'error': 'Gasto no encontrado o eliminado'}), 404

        category = session.query(Category).filter_by(categoriesid=expense.categoryid).first()
        if not category:
            return jsonify({'error': 'Categoría no encontrada'}), 404

    return jsonify({
        'amount': expense.amount,
        'categoryName': category.categoryname,
        'description': expense.description,
        'created': str(expense.created)[:10]
    }), 200