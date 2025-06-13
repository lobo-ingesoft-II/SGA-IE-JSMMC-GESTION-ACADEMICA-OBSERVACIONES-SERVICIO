from sqlalchemy.orm import Session
from app.models.observaciones import Observacion
from app.schemas.observaciones import ObservacionCreate

def create_observacion(db: Session, observacion: ObservacionCreate):
    db_observacion = Observacion(**observacion.dict())
    db.add(db_observacion)
    db.commit()
    db.refresh(db_observacion)
    return db_observacion

def get_observacion(db: Session, id_observacion: int):
    return db.query(Observacion).filter(Observacion.id_observacion == id_observacion).first()

def list_observaciones(db: Session):
    return db.query(Observacion).all()