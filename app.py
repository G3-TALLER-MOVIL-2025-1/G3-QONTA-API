from flask import Flask
from config import Config
from db import bcrypt, Base, engine
from flask_cors import CORS
from models import *
# from sqlalchemy.orm import sessionmaker

from routes.users import users_bp
from routes.expenses import expenses_bp
from routes.categories import categories_bp

app = Flask(__name__)
# app.config.from_object(Config)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db.init_app(app)
bcrypt.init_app(app)
CORS(app)

# Registrar rutas
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
app.register_blueprint(categories_bp, url_prefix='/api/categories')

@app.route('/')
def home():
    print("Usando base de datos:", engine.url)
    return {'status': 'API funcionando'}

if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        # db.create_all()
    app.run(debug=True)
