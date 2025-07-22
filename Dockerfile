# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia archivos necesarios
COPY requirements.txt .
COPY .env .


# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la app
COPY app/ app/


# Expone el puerto
EXPOSE 8006

# Ejecuta la aplicación
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8006"]
