# syntax=docker/dockerfile:1

# Usar una imagen base de Python ligera y moderna
FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Asegurar que la salida de Python se muestre inmediatamente
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos del proyecto al directorio de trabajo
COPY . .

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8080

# Comando para ejecutar el servidor Uvicorn, que servirá la aplicación 'app' desde el archivo 'main.py'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]