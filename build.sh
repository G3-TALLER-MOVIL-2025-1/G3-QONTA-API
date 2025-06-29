#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

echo "▶ Instalando Tesseract OCR…"
apt-get update
apt-get install -y tesseract-ocr

echo "▶ Verificando instalación…"
which tesseract        # ➜ debe mostrar /usr/bin/tesseract
tesseract --version    # ➜ debe imprimir versión

echo "▶ Instalando dependencias Python…"
pip install -r requirements.txt