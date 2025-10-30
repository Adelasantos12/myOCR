# Imagen base con Python
FROM python:3.10-slim

# Instalar Tesseract OCR y librerías necesarias
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev poppler-utils

# Crear directorio de trabajo
WORKDIR /app

# Copiar todo el contenido del proyecto
COPY . /app

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Configurar variables de entorno
ENV PORT=5000

# Exponer el puerto
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]