import os
import re
import shutil
import numpy as np
from PIL import Image, ImageOps
from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
import pytesseract

# ---------- Configuración inicial ----------
tesseract_path = shutil.which("tesseract")
if not tesseract_path:
    raise RuntimeError("Tesseract no está en PATH; revisa tu build.")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# ---------- Carga de modelo ----------
model_path = os.path.abspath('AIModel.h5')
amount_model = load_model(model_path)

# ---------- Blueprint ----------
ocr_bp = Blueprint('ocr', __name__)

# -- Endpoint con modelo CNN --
@ocr_bp.route('/scanImageWithModel', methods=['POST'])
def scan_image_with_model():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró la imagen en el request'}), 400
    try:
        image = Image.open(request.files['image'].stream).convert('RGB')
        image = image.resize((180, 180))
        img_array = np.expand_dims(np.array(image) / 255.0, axis=0)
        amount = round(float(amount_model.predict(img_array)[0][0]), 2)
        return jsonify({'message': 'Monto predicho con modelo', 'amount': amount}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -- Endpoint con Tesseract OCR --
@ocr_bp.route('/scanImageWithOCR', methods=['POST'])
def scan_image_with_ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró la imagen en el request'}), 400
    try:
        image = Image.open(request.files['image'].stream).convert('L')
        image = ImageOps.autocontrast(image)
        text = pytesseract.image_to_string(image)
        amounts = re.findall(r'[0-9]+(?:[.,][0-9]{1,2})?', text)
        return jsonify({
            'message': 'Texto extraído con OCR',
            'text': text.strip(),
            'possibleAmounts': amounts
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
