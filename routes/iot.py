from flask import Flask, request, jsonify, Blueprint
import joblib
import numpy as np

iot_bp = Blueprint('iot', __name__)

# Cargar modelo entrenado
modelo = joblib.load("modelo_riego.joblib")

@iot_bp.route('/predict_riego', methods=['POST'])
def predict_riego():
    data = request.json

    # Validación de entrada mínima
    required_fields = ["Temperatura", "Humedad", "Humedad_suelo"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    try:
        # Convertir datos a array numpy
        features = np.array([
            [float(data["Temperatura"]),
             float(data["Humedad"]),
             float(data["Humedad_suelo"])]
        ])

        # Realizar predicción
        pred = modelo.predict(features)[0]
        return jsonify({"riego": bool(pred)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

