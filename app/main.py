from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import time
from app.routers import observaciones
from app.db import init_db, test_connection
from app.services.estudiantes_client import estudiantes_client

# Librerias para Observabilidad
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from app.routers.observaciones import REQUEST_COUNT_OBSERVACIONES_ROUTERS, REQUEST_LATENCY_OBSERVACIONES_ROUTERS, ERROR_COUNT_OBSERVACIONES_ROUTERS

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Observaciones Disciplinarias",
    description="""
API REST para el registro y gestión de observaciones disciplinarias de estudiantes.

**Características Principales:**
• Validación automática de estudiantes
• Integración robusta con microservicios  
• Estadísticas avanzadas por estudiante
• Búsquedas eficientes con múltiples filtros
• Paginación optimizada para grandes datasets
• Manejo de errores robusto y descriptivo

**Flujo de Trabajo:**
1. Usuario selecciona estudiante de la lista
2. Se abre formulario con campos pre-cargados
3. Sistema verifica datos automáticamente
4. Observación se guarda con validaciones completas
5. Se retorna información completa y estructurada

**Arquitectura:** SOFEA (Service Oriented Front-End Architecture)
**Base de datos:** MySQL con índices optimizados
**Integración:** APIs de Estudiantes, Asignaturas y Autenticación
    """,
    version="2.0.0",
    contact={
        "name": "Equipo de Desarrollo - IEDT José Manuel Marroquín Caicedo",
        "email": "desarrollo@institucion.edu.co"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Configurar CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Middleware para observabilidad
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Log de petición entrante
    logger.info(f"🔄 {request.method} {request.url.path} - Cliente: {request.client.host}")
    
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        # Log de error en el middleware
        process_time = time.time() - start_time
        logger.error(f"❌ {request.method} {request.url.path} - Error: {str(e)} - Tiempo: {process_time:.3f}s")
        raise e
    finally:
        latency = time.time() - start_time
        endpoint = request.url.path
        method = request.method

        REQUEST_COUNT_OBSERVACIONES_ROUTERS.labels(endpoint=endpoint, method=method).inc()
        REQUEST_LATENCY_OBSERVACIONES_ROUTERS.labels(endpoint=endpoint, method=method).observe(latency)

        if status >= 400:
            ERROR_COUNT_OBSERVACIONES_ROUTERS.labels(endpoint=endpoint, method=method, status_code=str(status)).inc()
        
        # Log de respuesta
        logger.info(f"✅ {method} {endpoint} - Status: {status} - Tiempo: {latency:.3f}s")

    return response

# Manejo de errores de validación personalizados
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"❌ Error de validación en {request.url.path}: {exc.errors()}")
    
    # Procesar errores de validación de manera segura
    processed_errors = []
    for error in exc.errors():
        # Crear una copia del error sin objetos no serializables
        processed_error = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "input": error.get("input")
        }
        
        # Procesar el contexto de manera segura
        if "ctx" in error and error["ctx"]:
            processed_error["ctx"] = {}
            for key, value in error["ctx"].items():
                if isinstance(value, Exception):
                    processed_error["ctx"][key] = str(value)
                else:
                    processed_error["ctx"][key] = value
        
        processed_errors.append(processed_error)
    
    return JSONResponse(
        status_code=422,
        content={
            "message": "Error de validación en los datos enviados",
            "details": processed_errors,
            "success": False
        }
    )

# Manejo de errores ValueError y otros errores no serializables
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.error(f"❌ Error de valor en {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=400,
        content={
            "message": "Error en los datos proporcionados",
            "details": str(exc),
            "success": False
        }
    )

# Manejo de errores genéricos
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Error interno en {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "message": "Error interno del servidor",
            "details": "Ha ocurrido un error inesperado. Por favor, contacte al administrador.",
            "success": False
        }
    )

@app.on_event("startup")
async def startup_event():
    """Eventos de inicio de la aplicación"""
    logger.info("🚀 Iniciando Observaciones API...")
    
    try:
        init_db()
        test_connection()
        logger.info("✅ Base de datos inicializada correctamente")
        logger.info("🎯 Observaciones API iniciada correctamente")
    except Exception as e:
        logger.error(f"❌ Error en startup: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos de cierre de la aplicación"""
    logger.info("🔄 Cerrando Observaciones API...")
    
    try:
        await estudiantes_client.close()
        logger.info("✅ Recursos liberados correctamente")
    except Exception as e:
        logger.error(f"❌ Error en shutdown: {str(e)}")

# Incluir routers
app.include_router(observaciones.router, tags=["observaciones"])

# Health check endpoint
@app.get("/health", tags=["info"])
async def health_check():
    """Health check para monitoreo del servicio"""
    from datetime import datetime
    return {
        "message": "Servicio de observaciones funcionando correctamente",
        "success": True,
        "data": {
            "service": "observaciones-api",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat()
        }
    }

# Endpoint raíz con información de la API
@app.get("/", tags=["info"])
async def root():
    """Información básica de la API"""
    return {
        "message": "API de Observaciones - Sistema de Gestión Académica",
        "version": "2.0.0",
        "status": "active",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "architecture": "SOFEA (Service Oriented Front-End Architecture)",
        "microservices": {
            "estudiantes": "✅ Integrado",
            "asignaturas": "🔗 Referenciado",
            "autenticacion": "🔗 Referenciado"
        }
    }

# Endpoint de información de estado
@app.get("/info", tags=["info"])
async def api_info():
    """Información detallada de la API para el frontend"""
    return {
        "service_name": "observaciones-api",
        "version": "2.0.0",
        "environment": "development",
        "endpoints": {
            "create_observacion": "POST /observaciones/",
            "get_observacion": "GET /observaciones/{id}",
            "list_observaciones": "GET /observaciones/",
            "observaciones_by_estudiante": "GET /observaciones/estudiante/{id}",
            "estadisticas_estudiante": "GET /observaciones/estadisticas/estudiante/{id}",
            "tipos_falta": "GET /observaciones/tipos-falta/disponibles"
        },
        "external_dependencies": {
            "estudiantes_api": "http://localhost:8005",
            "database": "MySQL - observaciones_db"
        }
    }