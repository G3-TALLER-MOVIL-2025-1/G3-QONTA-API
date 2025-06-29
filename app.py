from flask import Flask
from flask_cors import CORS
from config import Config
from db import bcrypt, Base, engine
from models import *
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
from routes.users import users_bp
from routes.expenses import expenses_bp
from routes.categories import categories_bp
from routes.ocr import ocr_bp

app = Flask(__name__)
app.config.from_object(Config)

bcrypt.init_app(app)
CORS(app)

# Registrar rutas
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
app.register_blueprint(categories_bp, url_prefix='/api/categories')
app.register_blueprint(ocr_bp, url_prefix='/api/ocr')

@app.route('/')
def home():
    print("Usando base de datos:", engine.url)
    return {'status': 'API Live'}

# app.py (fragmento final)
with app.app_context():
    Base.metadata.create_all(bind=engine)

    #app.run(debug=True)
