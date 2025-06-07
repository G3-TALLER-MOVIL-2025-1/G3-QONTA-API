from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import Category
from datetime import datetime

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/register', methods=['POST'])
def registerCategory():
    data = request.get_json()

    required_fields = ['userId', 'categoryName', 'color']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    with SessionLocal() as session:
        new_category = Category(
            userid=data['userId'],
            categoryname=data['categoryName'],
            color=data['color'],
            created=datetime.utcnow(),
            creator=data['userId']
        )
        session.add(new_category)
        session.commit()

        return jsonify({
            'message': 'Categoría registrada correctamente',
            'categoryId': new_category.categoriesid
        }), 201

@categories_bp.route('/getAllCategoriesByUser', methods=['POST'])
def getAllCategoriesByUser():
    data = request.get_json()

    if not data or 'userId' not in data:
        return jsonify({'error': 'Debe proporcionar el userid'}), 400

    userId = int(data['userId'])

    with SessionLocal() as session:
        categories = session.query(Category).filter_by(userid=userId, isdeleted=False).all()

        result = [{
            'categoriesId': category.categoriesid,
            'categoryName': category.categoryname,
            'color': category.color,
            'created': category.created.isoformat() if category.created else None
        } for category in categories]

    return jsonify(result), 200
