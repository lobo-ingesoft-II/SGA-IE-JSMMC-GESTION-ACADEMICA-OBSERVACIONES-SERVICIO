"""
Script para inicializar la base de datos de observaciones
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.config import settings
from app.models.observaciones import Base

def create_database():
    """Crear la base de datos si no existe"""
    # Conectar sin especificar la base de datos
    base_url = settings.mysql_url.rsplit('/', 1)[0]
    engine = create_engine(base_url)
    
    with engine.connect() as connection:
        # Crear la base de datos si no existe
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}"))
        print(f"Base de datos '{settings.DB_NAME}' creada o ya existe")

def create_tables():
    """Crear las tablas en la base de datos"""
    engine = create_engine(settings.mysql_url)
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente")

def init_database():
    """Inicializar la base de datos completa"""
    try:
        create_database()
        create_tables()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
