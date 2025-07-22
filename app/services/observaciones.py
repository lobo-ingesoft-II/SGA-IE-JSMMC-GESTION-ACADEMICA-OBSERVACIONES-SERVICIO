from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
from datetime import date
from app.models.observaciones import Observacion
from app.schemas.observaciones import ObservacionCreate, ObservacionUpdate
from app.services.estudiantes_client import estudiantes_client

def create_observacion(db: Session, observacion: ObservacionCreate):
    """Crear una nueva observación"""
    db_observacion = Observacion(**observacion.dict())
    db.add(db_observacion)
    db.commit()
    db.refresh(db_observacion)
    return db_observacion

def get_observacion(db: Session, id_observacion: int):
    """Obtener una observación por ID"""
    return db.query(Observacion).filter(Observacion.id_observacion == id_observacion).first()

def list_observaciones(db: Session, skip: int = 0, limit: int = 100):
    """Listar todas las observaciones con paginación"""
    return db.query(Observacion).order_by(desc(Observacion.fecha_registro)).offset(skip).limit(limit).all()

def get_observaciones_by_estudiante(db: Session, id_estudiante: int, skip: int = 0, limit: int = 100):
    """Obtener observaciones de un estudiante específico"""
    return db.query(Observacion).filter(
        Observacion.id_estudiante == id_estudiante
    ).order_by(desc(Observacion.fecha_registro)).offset(skip).limit(limit).all()

def get_observaciones_by_profesor(db: Session, id_profesor: int, skip: int = 0, limit: int = 100):
    """Obtener observaciones registradas por un profesor específico"""
    return db.query(Observacion).filter(
        Observacion.id_profesor == id_profesor
    ).order_by(desc(Observacion.fecha_registro)).offset(skip).limit(limit).all()

def get_observaciones_by_asignatura(db: Session, id_asignatura: int, skip: int = 0, limit: int = 100):
    """Obtener observaciones de una asignatura específica"""
    return db.query(Observacion).filter(
        Observacion.id_asignatura == id_asignatura
    ).order_by(desc(Observacion.fecha_registro)).offset(skip).limit(limit).all()

def get_observaciones_by_tipo_falta(db: Session, tipo_falta: str, skip: int = 0, limit: int = 100):
    """Obtener observaciones por tipo de falta"""
    return db.query(Observacion).filter(
        Observacion.tipo_falta == tipo_falta
    ).order_by(desc(Observacion.fecha_registro)).offset(skip).limit(limit).all()

def get_observaciones_by_fecha_range(db: Session, fecha_inicio: date, fecha_fin: date, skip: int = 0, limit: int = 100):
    """Obtener observaciones en un rango de fechas"""
    return db.query(Observacion).filter(
        and_(
            Observacion.fecha_incidente >= fecha_inicio,
            Observacion.fecha_incidente <= fecha_fin
        )
    ).order_by(desc(Observacion.fecha_registro)).offset(skip).limit(limit).all()

def update_observacion(db: Session, id_observacion: int, observacion_update: ObservacionUpdate):
    """Actualizar una observación existente"""
    db_observacion = get_observacion(db, id_observacion)
    if not db_observacion:
        return None
    
    update_data = observacion_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_observacion, field, value)
    
    db.commit()
    db.refresh(db_observacion)
    return db_observacion

def delete_observacion(db: Session, id_observacion: int):
    """Eliminar una observación"""
    db_observacion = get_observacion(db, id_observacion)
    if not db_observacion:
        return None
    
    db.delete(db_observacion)
    db.commit()
    return db_observacion

def count_observaciones(db: Session):
    """Contar el total de observaciones"""
    return db.query(Observacion).count()

def count_observaciones_by_estudiante(db: Session, id_estudiante: int):
    """Contar observaciones de un estudiante"""
    return db.query(Observacion).filter(Observacion.id_estudiante == id_estudiante).count()

async def verificar_estudiante_existe(id_estudiante: int) -> bool:
    """Verificar si un estudiante existe en la API de estudiantes"""
    return await estudiantes_client.verificar_estudiante_existe(id_estudiante)

async def get_info_estudiante(id_estudiante: int):
    """Obtener información del estudiante desde la API de estudiantes"""
    return await estudiantes_client.get_estudiante_info(id_estudiante)