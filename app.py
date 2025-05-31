from flask import Flask
from config import Config
from db import db, bcrypt
from flask_cors import CORS
from models import *

from routes.users import users_bp
from routes.categories import categories_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
CORS(app)

# Registrar rutas
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(categories_bp, url_prefix='/api/categories')

@app.route('/')
def home():
    print("Usando base de datos:", db.engine.url)
    return {'status': 'API funcionando'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
