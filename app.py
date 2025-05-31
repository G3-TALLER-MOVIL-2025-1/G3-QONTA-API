from flask import Flask
from flask_cors import CORS
from config import Config
from db import bcrypt, Base, engine
from models import *
from routes.users import users_bp
from routes.expenses import expenses_bp
from routes.categories import categories_bp

app = Flask(__name__)
app.config.from_object(Config)

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
        # Crea las tablas si no existen en la base de datos (útil en Render)
        Base.metadata.create_all(bind=engine)
    app.run(debug=True)
