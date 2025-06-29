FROM python:3.10-slim

# Instala Tesseract y dependencias del sistema
RUN apt-get update && \
    apt-get install -y tesseract-ocr libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Crea y usa un directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto y comando de inicio
CMD ["gunicorn", "wsgi:app"]