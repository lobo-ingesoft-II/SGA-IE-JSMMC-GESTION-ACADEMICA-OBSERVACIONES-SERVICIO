from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy.sql import func
from app.db import Base

class Observacion(Base):
    __tablename__ = "observaciones"

    id_observacion = Column(Integer, primary_key=True, index=True)
    id_estudiante = Column(Integer, nullable=False)
    id_asignatura = Column(Integer, nullable=False)
    id_profesor = Column(Integer, nullable=False)
    fecha_incidente = Column(Date, nullable=False)
    tipo_falta = Column(String(50), nullable=False)
    articulo_manual_convivencia = Column(String(255), nullable=True)
    observacion = Column(Text, nullable=False)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)