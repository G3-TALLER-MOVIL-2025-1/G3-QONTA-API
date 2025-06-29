import os
import re
import shutil
import numpy as np
from PIL import Image, ImageOps
from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
import pytesseract


# ─────────────────────────────────────────────
#  Configuración inicial de Tesseract
# ─────────────────────────────────────────────
tesseract_path = shutil.which("tesseract")
if not tesseract_path:
    raise RuntimeError("Tesseract no está en PATH; revisa tu build.")
pytesseract.pytesseract.tesseract_cmd = tesseract_path


# ─────────────────────────────────────────────
#  Carga de modelo CNN (.h5)
# ─────────────────────────────────────────────
model_path = os.path.abspath("AIModel.h5")
amount_model = load_model(model_path)


# ─────────────────────────────────────────────
#  Blueprint
# ─────────────────────────────────────────────
ocr_bp = Blueprint("ocr", __name__)


# ─────────────────────────────────────────────
#  Endpoint: CNN para clasificación/regresión
# ─────────────────────────────────────────────
@ocr_bp.route("/scanImageWithModel", methods=["POST"])
def scan_image_with_model():
    if "image" not in request.files:
        return jsonify({"error": "No se encontró la imagen en el request"}), 400
    try:
        image = Image.open(request.files["image"].stream).convert("RGB")
        image = image.resize((180, 180))
        img_array = np.expand_dims(np.array(image) / 255.0, axis=0)

        prediction = amount_model.predict(img_array)
        amount = round(float(prediction[0][0]), 2)

        return jsonify(
            {
                "message": "Monto predicho con modelo",
                "amount": amount,
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
#  Endpoint: OCR con Tesseract (Yape / Plin)
# ─────────────────────────────────────────────
@ocr_bp.route("/scanImageWithOCR", methods=["POST"])
def scan_image_with_ocr():
    if "image" not in request.files:
        return jsonify({"error": "No se encontró la imagen en el request"}), 400
    try:
        # 1) Preprocesamiento ligero
        image = Image.open(request.files["image"].stream).convert("L")
        image = ImageOps.autocontrast(image)

        # 2) OCR
        raw_text = pytesseract.image_to_string(image)

        # 3) Buscar montos precedidos por 'S/'  -> S/ 3   ó   S/ 171.92
        pattern = r"S\/\s?(\d+(?:[.,]\d{1,2})?)"
        matches = re.findall(pattern, raw_text, flags=re.IGNORECASE)

        if not matches:
            return (
                jsonify(
                    {
                        "message": "No se detectó monto en el formato esperado",
                        "rawText": raw_text.strip(),
                    }
                ),
                404,
            )

        # Tomamos el primer valor encontrado y normalizamos ',' → '.'
        amount_str = matches[0].replace(",", ".")
        amount = round(float(amount_str), 2)

        return jsonify(
            {
                "message": "Monto extraído correctamente",
                "amount": amount,
                "allMatches": [m.replace(",", ".") for m in matches],
            }
        ), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
