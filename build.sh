#!/usr/bin/env bash

# Instala Tesseract OCR
apt-get update
apt-get install -y tesseract-ocr

# Instala dependencias de Python
pip install -r requirements.txt