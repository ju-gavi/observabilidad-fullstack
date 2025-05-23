FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# ✅ Crear el directorio de logs en tiempo de build
RUN mkdir -p /var/log/flask

EXPOSE 5000

# Ejecuta la aplicación Flask
CMD ["python", "main.py"]


