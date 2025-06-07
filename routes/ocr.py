import re
from flask import Blueprint, request, jsonify
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/scanImageForAmount', methods=['POST'])
def scan_image_for_amount():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró la imagen en el request'}), 400

    image_file = request.files['image']

    try:
        image = Image.open(image_file.stream)
        text = pytesseract.image_to_string(image)
        lines = text.splitlines()

        def normalize_to_float(val):
            try:
                return float(val.replace(',', '.'))
            except:
                return None

        # Paso 1: Buscar "S/ 150" o "S/. 150.90"
        regex_s = re.findall(r'S/?\.?\s*(-?\d+(?:[.,]\d{1,2})?)', text, re.IGNORECASE)
        probable_total = normalize_to_float(regex_s[0]) if regex_s else None

        # Paso 2: Palabras clave como "TOTAL" o "SON" (evitando DESCUENTO)
        if probable_total is None:
            for line in lines:
                upper = line.upper()
                if ('TOTAL' in upper or 'SON' in upper) and 'DESCUENTO' not in upper:
                    found = re.findall(r'(-?\d+(?:[.,]\d{1,2}))', line)
                    if found:
                        probable_total = normalize_to_float(found[-1])
                        if probable_total is not None:
                            break

        # Paso 3: Últimos renglones como fallback si aún no se detecta
        if probable_total is None:
            for line in reversed(lines[-6:]):
                found = re.findall(r'(-?\d+(?:[.,]\d{1,2}))', line)
                if found:
                    probable_total = normalize_to_float(found[-1])
                    if probable_total is not None:
                        break

        # Paso 4: Recolectar todos los números (evitar falsos positivos largos)
        all_matches_raw = re.findall(r'(?<!\d)(-?\d+(?:[.,]\d{1,2})?)(?!\d)', text)
        all_matches = []
        for m in all_matches_raw:
            f = normalize_to_float(m)
            if f is not None and 0 <= f < 1_000_000:
                all_matches.append(f)

        # Paso 5: fallback si aún no se tiene probable_total
        if probable_total is None:
            if all_matches:
                probable_total = max(all_matches)
            else:
                return jsonify({
                    'message': 'No se encontró ningún monto',
                    'allMatches': [],
                    'rawText': text
                }), 200

        return jsonify({
            'message': 'Monto detectado',
            'amount': probable_total,
            'allMatches': all_matches,
            'rawText': text
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
