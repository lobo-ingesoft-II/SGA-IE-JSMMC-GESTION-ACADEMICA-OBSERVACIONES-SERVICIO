from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.observaciones import ObservacionCreate, ObservacionResponse
from app.services.observaciones import create_observacion, get_observacion, list_observaciones
from app.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ObservacionResponse)
def create(observacion: ObservacionCreate, db: Session = Depends(get_db)):
    return create_observacion(db, observacion)

@router.get("/{id_observacion}", response_model=ObservacionResponse)
def get(id_observacion: int, db: Session = Depends(get_db)):
    db_observacion = get_observacion(db, id_observacion)
    if not db_observacion:
        raise HTTPException(status_code=404, detail="Observacion not found")
    return db_observacion

@router.get("/", response_model=list[ObservacionResponse])
def list_all(db: Session = Depends(get_db)):
    return list_observaciones(db)