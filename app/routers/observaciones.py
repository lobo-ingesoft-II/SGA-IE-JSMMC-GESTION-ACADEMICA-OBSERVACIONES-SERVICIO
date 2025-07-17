from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
import logging

# Librerias para Observabilidad
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from starlette.responses import Response
from prometheus_client import CollectorRegistry, generate_latest
from app.schemas.observaciones import (
    ObservacionCreate, 
    ObservacionResponse, 
    ObservacionUpdate,
    ObservacionDetallada
)
from app.services.observaciones import (
    create_observacion, 
    get_observacion, 
    list_observaciones,
    get_observaciones_by_estudiante,
    update_observacion,
    delete_observacion,
    verificar_estudiante_existe,
    get_info_estudiante
)
from app.db import SessionLocal

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/observaciones",
    tags=["observaciones"],
    responses={
        404: {"description": "Recurso no encontrado"},
        503: {"description": "Servicios externos no disponibles"},
        422: {"description": "Error de validación"}
    }
)

# Metricas 
REQUEST_COUNT_OBSERVACIONES_ROUTERS = Counter(
    "http_requests_total", 
    "TOTAL PETICIONES HTTP router-observaciones",
    ["method", "endpoint"]
)

REQUEST_LATENCY_OBSERVACIONES_ROUTERS = Histogram(
    "http_request_duration_seconds", 
    "DURACION DE LAS PETICIONES router-observaciones",
    ["method", "endpoint"],
    buckets=[0.1, 0.3, 1.0, 2.5, 5.0, 10.0]  
)

# 3. Errores por endpoint
ERROR_COUNT_OBSERVACIONES_ROUTERS = Counter(
    "http_request_errors_total",
    "TOTAL ERRORES HTTP (status >= 400)",
    ["endpoint", "method", "status_code"]
)

# Ruta para observabilidad 
@router.get("/custom_metrics")
def custom_metrics():
    registry = CollectorRegistry()
    registry.register(REQUEST_COUNT_OBSERVACIONES_ROUTERS)
    registry.register(REQUEST_LATENCY_OBSERVACIONES_ROUTERS)
    registry.register(ERROR_COUNT_OBSERVACIONES_ROUTERS)
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== ENDPOINTS PRINCIPALES ====================

@router.get(
    "/",
    response_model=List[ObservacionResponse],
    summary="Listar observaciones con paginación",
    description="Obtiene lista paginada de todas las observaciones registradas"
)
def list_observaciones_endpoint(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Listar observaciones con paginación.
    
    **Información para Frontend:**
    - Usar para mostrar tabla principal de observaciones
    - Implementar paginación en el cliente
    - Cada observación incluye información del estudiante integrada
    """
    try:
        logger.info(f"📋 Listando observaciones - Skip: {skip}, Limit: {limit}")
        
        observaciones = list_observaciones(db, skip=skip, limit=limit)
        
        # Convertir a schemas de respuesta con manejo de errores de validación
        observaciones_response = []
        for obs in observaciones:
            try:
                obs_dict = {
                    "id_observacion": obs.id_observacion,
                    "id_estudiante": obs.id_estudiante,
                    "id_asignatura": obs.id_asignatura,
                    "id_profesor": obs.id_profesor,
                    "fecha_incidente": obs.fecha_incidente,
                    "tipo_falta": obs.tipo_falta,
                    "articulo_manual_convivencia": obs.articulo_manual_convivencia,
                    "observacion": obs.observacion,
                    "fecha_registro": obs.fecha_registro
                }
                observacion_response = ObservacionResponse(**obs_dict)
                observaciones_response.append(observacion_response)
            except Exception as validation_error:
                logger.error(f"Error de validación en observación {obs.id_observacion}: {str(validation_error)}")
                # Continuar con las demás observaciones
                continue
        
        logger.info(f"✅ Observaciones obtenidas exitosamente: {len(observaciones_response)} registros")
        return observaciones_response
        
    except Exception as e:
        logger.error(f"❌ Error al listar observaciones: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post(
    "/",
    response_model=ObservacionDetallada,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva observación",
    description="Registra una nueva observación disciplinaria con validación automática del estudiante"
)
def create_observacion_endpoint(
    observacion: ObservacionCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva observación disciplinaria.
    
    **Flujo de Validación:**
    1. Verifica que el estudiante exista en la API de estudiantes
    2. Valida los datos de entrada
    3. Registra la observación en la base de datos
    4. Retorna información completa con datos del estudiante
    
    **Para el Frontend:**
    - Usar después de validar el formulario
    - Mostrar mensaje de éxito/error según respuesta
    - Incluir datos del estudiante en la respuesta
    """
    try:
        logger.info(f"📝 Creando observación para estudiante ID: {observacion.id_estudiante}")
        
        # Verificar que el estudiante existe
        estudiante_info = verificar_estudiante_existe(observacion.id_estudiante)
        if not estudiante_info:
            logger.warning(f"⚠️ Estudiante no encontrado: ID {observacion.id_estudiante}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El estudiante con ID {observacion.id_estudiante} no existe"
            )
        
        # Crear la observación
        nueva_observacion = create_observacion(db, observacion)
        
        # Preparar respuesta con información del estudiante (simplificado por ahora)
        # estudiante_info = get_info_estudiante(nueva_observacion.id_estudiante)
        estudiante_info = None  # Por ahora simplificado
        
        observacion_detallada = ObservacionDetallada(
            id_observacion=nueva_observacion.id_observacion,
            id_estudiante=nueva_observacion.id_estudiante,
            id_asignatura=nueva_observacion.id_asignatura,
            id_profesor=nueva_observacion.id_profesor,
            fecha_incidente=nueva_observacion.fecha_incidente,
            tipo_falta=nueva_observacion.tipo_falta,
            articulo_manual_convivencia=nueva_observacion.articulo_manual_convivencia,
            observacion=nueva_observacion.observacion,
            fecha_registro=nueva_observacion.fecha_registro,
            estudiante_info=estudiante_info
        )
        
        logger.info(f"✅ Observación creada exitosamente: ID {nueva_observacion.id_observacion}")
        return observacion_detallada
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al crear observación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get(
    "/{id_observacion}",
    response_model=ObservacionDetallada,
    summary="Obtener observación detallada",
    description="Obtiene una observación específica con información completa del estudiante"
)
def get_observacion_endpoint(
    id_observacion: int,
    db: Session = Depends(get_db)
):
    """
    Obtener observación detallada por ID.
    
    **Para el Frontend:**
    - Usar para mostrar detalles completos
    - Incluye información del estudiante integrada
    - Ideal para modal de detalles o página de edición
    """
    try:
        logger.info(f"🔍 Buscando observación ID: {id_observacion}")
        
        observacion = get_observacion(db, id_observacion)
        if not observacion:
            logger.warning(f"⚠️ Observación no encontrada: ID {id_observacion}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Observación con ID {id_observacion} no encontrada"
            )
        
        # Obtener información del estudiante (simplificado por ahora)
        # estudiante_info = get_info_estudiante(observacion.id_estudiante)
        estudiante_info = None  # Por ahora simplificado
        
        # Preparar respuesta detallada
        observacion_detallada = ObservacionDetallada(
            id_observacion=observacion.id_observacion,
            id_estudiante=observacion.id_estudiante,
            id_asignatura=observacion.id_asignatura,
            id_profesor=observacion.id_profesor,
            fecha_incidente=observacion.fecha_incidente,
            tipo_falta=observacion.tipo_falta,
            articulo_manual_convivencia=observacion.articulo_manual_convivencia,
            observacion=observacion.observacion,
            fecha_registro=observacion.fecha_registro,
            estudiante_info=estudiante_info
        )
        
        logger.info(f"✅ Observación encontrada exitosamente: ID {id_observacion}")
        return observacion_detallada
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al obtener observación {id_observacion}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put(
    "/{id_observacion}",
    response_model=ObservacionDetallada,
    summary="Actualizar observación",
    description="Actualiza una observación existente (solo campos modificables)"
)
def update_observacion_endpoint(
    id_observacion: int,
    observacion_update: ObservacionUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar observación existente.
    
    **Campos Actualizables:**
    - fecha_incidente
    - tipo_falta
    - articulo_manual_convivencia
    - observacion
    
    **Para el Frontend:**
    - Usar en formulario de edición
    - Validar permisos antes de permitir edición
    - Mostrar confirmación de cambios
    """
    try:
        logger.info(f"✏️ Actualizando observación ID: {id_observacion}")
        
        # Verificar que la observación existe
        observacion_existente = get_observacion(db, id_observacion)
        if not observacion_existente:
            logger.warning(f"⚠️ Observación no encontrada para actualizar: ID {id_observacion}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Observación con ID {id_observacion} no encontrada"
            )
        
        # Actualizar la observación
        observacion_actualizada = update_observacion(db, id_observacion, observacion_update)
        
        # Obtener información del estudiante (simplificado por ahora)
        # estudiante_info = get_info_estudiante(observacion_actualizada.id_estudiante)
        estudiante_info = None  # Por ahora simplificado
        
        # Preparar respuesta detallada
        observacion_detallada = ObservacionDetallada(
            id_observacion=observacion_actualizada.id_observacion,
            id_estudiante=observacion_actualizada.id_estudiante,
            id_asignatura=observacion_actualizada.id_asignatura,
            id_profesor=observacion_actualizada.id_profesor,
            fecha_incidente=observacion_actualizada.fecha_incidente,
            tipo_falta=observacion_actualizada.tipo_falta,
            articulo_manual_convivencia=observacion_actualizada.articulo_manual_convivencia,
            observacion=observacion_actualizada.observacion,
            fecha_registro=observacion_actualizada.fecha_registro,
            estudiante_info=estudiante_info
        )
        
        logger.info(f"✅ Observación actualizada exitosamente: ID {id_observacion}")
        return observacion_detallada
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al actualizar observación {id_observacion}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete(
    "/{id_observacion}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar observación",
    description="Elimina una observación del sistema (operación irreversible)"
)
def delete_observacion_endpoint(
    id_observacion: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar observación del sistema.
    
    **Para el Frontend:**
    - Mostrar confirmación antes de eliminar
    - Usar solo con permisos administrativos
    - Actualizar lista después de eliminación exitosa
    """
    try:
        logger.info(f"🗑️ Eliminando observación ID: {id_observacion}")
        
        # Verificar que la observación exists
        observacion_existente = get_observacion(db, id_observacion)
        if not observacion_existente:
            logger.warning(f"⚠️ Observación no encontrada para eliminar: ID {id_observacion}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Observación con ID {id_observacion} no encontrada"
            )
        
        # Eliminar la observación
        success = delete_observacion(db, id_observacion)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la observación"
            )
        
        logger.info(f"✅ Observación eliminada exitosamente: ID {id_observacion}")
        # FastAPI maneja automáticamente el status 204 sin contenido
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al eliminar observación {id_observacion}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get(
    "/estudiante/{id_estudiante}",
    response_model=List[ObservacionResponse],
    summary="Observaciones por estudiante",
    description="Obtiene todas las observaciones de un estudiante específico"
)
def get_observaciones_by_estudiante_endpoint(
    id_estudiante: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Obtener observaciones de un estudiante específico.
    
    **Para el Frontend:**
    - Usar en perfil del estudiante
    - Mostrar historial disciplinario
    - Implementar paginación para historiales largos
    """
    try:
        logger.info(f"👤 Buscando observaciones del estudiante ID: {id_estudiante}")
        
        # Verificar que el estudiante existe
        estudiante_info = verificar_estudiante_existe(id_estudiante)
        if not estudiante_info:
            logger.warning(f"⚠️ Estudiante no encontrado: ID {id_estudiante}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El estudiante con ID {id_estudiante} no existe"
            )
        
        # Obtener observaciones del estudiante
        observaciones = get_observaciones_by_estudiante(db, id_estudiante, skip=skip, limit=limit)
        
        # Convertir a schemas de respuesta
        observaciones_response = []
        for obs in observaciones:
            obs_dict = {
                "id_observacion": obs.id_observacion,
                "id_estudiante": obs.id_estudiante,
                "id_asignatura": obs.id_asignatura,
                "id_profesor": obs.id_profesor,
                "fecha_incidente": obs.fecha_incidente,
                "tipo_falta": obs.tipo_falta,
                "articulo_manual_convivencia": obs.articulo_manual_convivencia,
                "observacion": obs.observacion,
                "fecha_registro": obs.fecha_registro
            }
            observacion_response = ObservacionResponse(**obs_dict)
            observaciones_response.append(observacion_response)
        
        logger.info(f"✅ Observaciones del estudiante obtenidas: {len(observaciones_response)} registros")
        return observaciones_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error al obtener observaciones del estudiante {id_estudiante}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
