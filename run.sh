#!/bin/bash

# Script para ejecutar el servicio de observaciones

echo "🚀 Iniciando servicio de Observaciones..."

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado. Por favor, configura las variables de entorno."
fi

# Verificar si las dependencias están instaladas
echo "📦 Verificando dependencias..."
pip install -r requirements.txt

# Inicializar la base de datos
echo "🗄️  Inicializando base de datos..."
python scripts/init_db.py

# Ejecutar el servicio
echo "🎯 Ejecutando servicio en puerto 8003..."
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
