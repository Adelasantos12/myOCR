# Usar una imagen base de Python delgada
FROM python:3.10-slim

# Instalar Tesseract OCR, el paquete de español y otras utilidades
# Limpiar la caché de apt para reducir el tamaño de la imagen
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar primero el archivo de dependencias para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Configurar la variable de entorno para el puerto, común en plataformas de despliegle
ENV PORT 5000

# Exponer el puerto
EXPOSE 5000

# Comando de inicio usando Gunicorn para un entorno de producción
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
