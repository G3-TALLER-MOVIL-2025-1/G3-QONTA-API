from flask import Blueprint, request, jsonify
from db import db
from models import Category, User
from datetime import datetime

categories_bp = Blueprint('categories', __name__)

# Crear una nueva categoría para un usuario
@categories_bp.route('/create', methods=['POST'])
def create_category():
    data = request.get_json()
    required_fields = ['USERID', 'CATEGORYNAME']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    user = User.query.filter_by(USERSID=data['USERID'], ISDELETED=False).first()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    category = Category(
        USERID=data['USERID'],
        CATEGORYNAME=data['CATEGORYNAME'],
        ICON=data.get('ICON', ''),  # opcional
        CREATED=datetime.utcnow(),
        CREATOR=data['USERID']
    )
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Categoría creada', 'CATEGORIESID': category.CATEGORIESID}), 201

# Obtener todas las categorías de un usuario
@categories_bp.route('/getByUser', methods=['POST'])
def get_categories_by_user():
    data = request.get_json()
    if not data or 'USERID' not in data:
        return jsonify({'error': 'Debe proporcionar USERID'}), 400

    categories = Category.query.filter_by(USERID=data['USERID'], ISDELETED=False).all()
    result = [{
        'CATEGORIESID': cat.CATEGORIESID,
        'CATEGORYNAME': cat.CATEGORYNAME,
        'ICON': cat.ICON
    } for cat in categories]

    return jsonify(result), 200

# Editar una categoría
@categories_bp.route('/edit', methods=['PUT'])
def edit_category():
    data = request.get_json()
    if not data or 'CATEGORIESID' not in data:
        return jsonify({'error': 'Debe proporcionar CATEGORIESID'}), 400

    category = Category.query.filter_by(CATEGORIESID=data['CATEGORIESID'], ISDELETED=False).first()
    if not category:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    category.CATEGORYNAME = data.get('CATEGORYNAME', category.CATEGORYNAME)
    category.ICON = data.get('ICON', category.ICON)
    category.CHANGED = datetime.utcnow()

    db.session.commit()

    return jsonify({'message': 'Categoría actualizada'}), 200

# Eliminar una categoría (soft delete)
@categories_bp.route('/delete', methods=['DELETE'])
def delete_category():
    data = request.get_json()
    if not data or 'CATEGORIESID' not in data:
        return jsonify({'error': 'Debe proporcionar CATEGORIESID'}), 400

    category = Category.query.filter_by(CATEGORIESID=data['CATEGORIESID'], ISDELETED=False).first()
    if not category:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    category.ISDELETED = True
    category.CHANGED = datetime.utcnow()

    db.session.commit()

    return jsonify({'message': 'Categoría eliminada'}), 200
