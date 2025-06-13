from pydantic import BaseModel
from datetime import date, datetime

class ObservacionBase(BaseModel):
    id_estudiante: int
    id_asignatura: int
    id_profesor: int
    fecha_incidente: date
    tipo_falta: str
    articulo_manual_convivencia: str | None
    observacion: str

class ObservacionCreate(ObservacionBase):
    pass

class ObservacionResponse(ObservacionBase):
    id_observacion: int
    fecha_registro: datetime

    class Config:
        orm_mode = True