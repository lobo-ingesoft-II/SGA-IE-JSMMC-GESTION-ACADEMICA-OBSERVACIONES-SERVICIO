from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List

class ObservacionBase(BaseModel):
    id_estudiante: int = Field(..., gt=0, description="ID del estudiante")
    id_asignatura: int = Field(..., gt=0, description="ID de la asignatura")
    id_profesor: int = Field(..., gt=0, description="ID del profesor")
    fecha_incidente: date = Field(..., description="Fecha del incidente")
    tipo_falta: str = Field(..., description="Tipo de falta: Leve, Grave, Gravísima")
    articulo_manual_convivencia: Optional[str] = Field(
        None, 
        max_length=100, 
        description="Artículo del manual de convivencia"
    )
    observacion: str = Field(
        ..., 
        min_length=10, 
        max_length=1000, 
        description="Descripción detallada de la observación"
    )
    
    @validator('fecha_incidente')
    def validate_fecha_incidente(cls, v):
        if v > date.today():
            raise ValueError('La fecha del incidente no puede ser futura')
        return v
    
    @validator('observacion')
    def validate_observacion(cls, v):
        if not v.strip():
            raise ValueError('La observación no puede estar vacía')
        return v.strip()

class ObservacionCreate(ObservacionBase):
    """Schema para crear observaciones desde el frontend"""
    pass

class ObservacionUpdate(BaseModel):
    """Schema para actualizar observaciones"""
    id_asignatura: Optional[int] = Field(None, gt=0)
    id_profesor: Optional[int] = Field(None, gt=0)
    fecha_incidente: Optional[date] = None
    tipo_falta: Optional[str] = None
    articulo_manual_convivencia: Optional[str] = Field(None, max_length=100)
    observacion: Optional[str] = Field(None, min_length=10, max_length=1000)
    
    @validator('fecha_incidente')
    def validate_fecha_incidente(cls, v):
        if v and v > date.today():
            raise ValueError('La fecha del incidente no puede ser futura')
        return v

class ObservacionResponse(ObservacionBase):
    """Schema para respuestas de observaciones"""
    id_observacion: int
    fecha_registro: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

class ObservacionListResponse(BaseModel):
    """Schema para listado paginado de observaciones"""
    observaciones: List[ObservacionResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

class EstudianteInfo(BaseModel):
    """Información básica del estudiante"""
    id_usuario: int
    id_acudiente: int
    fecha_nacimiento: str
    id_curso: int
    estado_matricula: str
    sede: str
    id_estudiante: int

class ObservacionDetallada(ObservacionResponse):
    """Schema para observaciones con información completa del estudiante"""
    estudiante_info: Optional[EstudianteInfo] = None

class EstadisticasEstudiante(BaseModel):
    """Schema para estadísticas de observaciones por estudiante"""
    id_estudiante: int
    total_observaciones: int
    tipos_falta_frecuentes: dict
    observaciones_por_mes: Optional[dict] = None
    tendencia: Optional[str] = None

class ResponseMessage(BaseModel):
    """Schema estándar para mensajes de respuesta"""
    message: str
    success: bool
    data: Optional[dict] = None
    estudiante_info: Optional[EstudianteInfo] = None