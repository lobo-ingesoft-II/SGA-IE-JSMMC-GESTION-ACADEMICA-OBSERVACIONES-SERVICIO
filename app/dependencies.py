from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.observaciones import verificar_estudiante_existe

def get_db():
    """Dependencia para obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def validate_estudiante_exists(id_estudiante: int):
    """Dependencia para validar que un estudiante existe"""
    if not await verificar_estudiante_existe(id_estudiante):
        raise HTTPException(
            status_code=404,
            detail=f"Estudiante con ID {id_estudiante} no encontrado"
        )
    return id_estudiante

def validate_pagination(skip: int = 0, limit: int = 100):
    """Dependencia para validar parámetros de paginación"""
    if skip < 0:
        raise HTTPException(status_code=400, detail="El parámetro 'skip' debe ser >= 0")
    if limit < 1 or limit > 1000:
        raise HTTPException(status_code=400, detail="El parámetro 'limit' debe estar entre 1 y 1000")
    
    return {"skip": skip, "limit": limit}
