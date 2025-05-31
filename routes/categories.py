from flask import Blueprint, jsonify

categories_bp = Blueprint('categories', __name__)

CATEGORIES = [
    {'id': 1, 'name': 'Alimentación'},
    {'id': 2, 'name': 'Transporte'},
    {'id': 3, 'name': 'Entretenimiento'},
    {'id': 4, 'name': 'Salud'},
    {'id': 5, 'name': 'Educación'},
    {'id': 6, 'name': 'Servicios'},
    {'id': 7, 'name': 'Otros'}
]

@categories_bp.route('/getCategories', methods=['GET'])
def get_categories():
    return jsonify(CATEGORIES), 200