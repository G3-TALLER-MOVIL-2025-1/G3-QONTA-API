import os
import numpy as np
from PIL import Image
from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

ocr_bp = Blueprint('ocr', __name__)

# Ruta al modelo .h5 en la raíz
model_path = os.path.abspath('AIModel.h5')
amount_model = load_model(model_path)

@ocr_bp.route('/scanImageWithModel', methods=['POST'])
def scan_image_with_model():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró la imagen en el request'}), 400

    try:
        image_file = request.files['image']
        image = Image.open(image_file.stream).convert('RGB')  # aseguramos RGB
        image = image.resize((180, 180))
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # (1, 128, 128, 3)

        prediction = amount_model.predict(img_array)
        amount = round(float(prediction[0][0]), 2)

        return jsonify({
            'message': 'Monto predicho con modelo',
            'amount': amount
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
