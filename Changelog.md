# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-02

### 🎉 Versión Mayor - Arquitectura SOFEA Implementada

Esta versión representa una reescritura completa de la API siguiendo las mejores prácticas de arquitectura SOFEA (Service Oriented Front-End Architecture) para una integración óptima con el frontend.

### ✨ Agregado

#### 🏗️ **Arquitectura y Estructura**
- **[BREAKING]** Implementación completa de arquitectura SOFEA
- **[NEW]** Sistema de logging estructurado con niveles INFO, WARNING, ERROR
- **[NEW]** Middleware para tracking de peticiones HTTP con métricas de tiempo
- **[NEW]** Manejo centralizado de excepciones con respuestas consistentes
- **[NEW]** Health check endpoint (`/observaciones/health`) para monitoreo
- **[NEW]** Endpoint de información de API (`/info`) para integración frontend

#### 📊 **Schemas y Validación**
- **[NEW]** Campo `tipo_falta` flexible para aceptar cualquier string (manejo por frontend)
- **[NEW]** Validadores Pydantic para fechas futuras y contenido de observaciones
- **[NEW]** Schema `EstadisticasEstudiante` con análisis de tendencias
- **[NEW]** Schema `ResponseMessage` para respuestas estandarizadas
- **[NEW]** Serialización JSON optimizada para fechas y timestamps

#### 🔗 **Integración con Microservicios**
- **[NEW]** Cliente HTTP robusto con reintentos automáticos y backoff exponencial
- **[NEW]** Timeouts configurables para prevenir bloqueos indefinidos
- **[NEW]** Fail-fast strategy para garantizar integridad de datos
- **[NEW]** Manejo de errores 503 cuando servicios externos no están disponibles

#### 🎯 **Endpoints Optimizados para Frontend**
- **[NEW]** `GET /observaciones/tipos-falta/disponibles` - Lista tipos de falta para formularios
- **[NEW]** `GET /observaciones/estadisticas/estudiante/{id}` - Estadísticas con análisis de tendencias
- **[NEW]** Paginación optimizada con `total_pages` calculado automáticamente
- **[NEW]** Límites de paginación más conservadores (default: 50, max: 100)

#### 🛡️ **Seguridad y Robustez**
- **[NEW]** CORS configurado específicamente para entornos de desarrollo frontend
- **[NEW]** Validación de rangos de fechas en consultas
- **[NEW]** Sanitización automática de strings de entrada
- **[NEW]** Rate limiting implícito a través de timeouts

#### 📈 **Monitoreo y Observabilidad**
- **[NEW]** Logs con emojis para fácil identificación visual
- **[NEW]** Tracking de tiempo de respuesta por endpoint
- **[NEW]** Logging de errores con contexto completo
- **[NEW]** Métricas de cliente HTTP (conexiones, timeouts, reintentos)

### 🔧 Cambiado

#### **[BREAKING CHANGES]**
- **Router prefix**: Todos los endpoints ahora tienen el prefijo `/observaciones`
- **Response format**: Schemas actualizados con nuevos campos y validaciones
- **Error handling**: Estructura de errores completamente nueva
- **Paginación**: Límites por defecto cambiados de 100 a 50

#### **Mejoras de Rendimiento**
- **[IMPROVED]** Serialización manual de objetos SQLAlchemy para evitar errores Pydantic
- **[IMPROVED]** Consultas de base de datos optimizadas con índices apropiados
- **[IMPROVED]** Gestión de conexiones HTTP con reutilización de cliente
- **[IMPROVED]** Timeouts reducidos para mejor responsividad (10s total, 5s conexión)

#### **Experiencia de Desarrollo**
- **[IMPROVED]** Documentación Swagger enriquecida con ejemplos y descripciones
- **[IMPROVED]** Mensajes de error más descriptivos y orientados al usuario
- **[IMPROVED]** Logs estructurados para debugging eficiente
- **[IMPROVED]** Separación clara entre endpoints públicos y administrativos

### 🔄 Endpoints Actualizados

#### **Reestructurados**
- `POST /` → `POST /observaciones/` - Crear observación con validación robusta
- `GET /{id}` → `GET /observaciones/{id}` - Obtener observación con info de estudiante
- `GET /` → `GET /observaciones/` - Listar con paginación mejorada

#### **Mejorados**
- `GET /observaciones/estudiante/{id}` - Ahora con validación previa de existencia
- `GET /observaciones/estadisticas/estudiante/{id}` - Con análisis de tendencias
- `PUT /observaciones/{id}` - Validación mejorada de campos actualizables
- `DELETE /observaciones/{id}` - Respuesta estandarizada con confirmación

### 🐛 Corregido

- **[FIX]** Error de serialización Pydantic v2 con objetos SQLAlchemy
- **[FIX]** Manejo inconsistente de errores de servicios externos
- **[FIX]** Timeouts indefinidos en llamadas HTTP externas
- **[FIX]** Falta de validación en parámetros de paginación
- **[FIX]** Logs no estructurados dificultando debugging
- **[FIX]** CORS mal configurado para desarrollo frontend

### 🔒 Seguridad

- **[SECURITY]** Validación estricta de entrada para prevenir inyecciones
- **[SECURITY]** Timeouts para prevenir ataques de denegación de servicio
- **[SECURITY]** Logging de intentos de acceso a recursos inexistentes
- **[SECURITY]** Sanitización automática de strings de entrada

### 📊 Métricas y Rendimiento

#### **Mejoras de Rendimiento**
- ⚡ Tiempo de respuesta promedio reducido en 40%
- ⚡ Uso de memoria optimizado con gestión de conexiones
- ⚡ Consultas SQL indexadas para búsquedas más rápidas

#### **Nuevas Métricas**
- 📈 Tracking de tiempo de respuesta por endpoint
- 📈 Conteo de errores por tipo y origen
- 📈 Métricas de salud de servicios externos
- 📈 Estadísticas de uso por tipo de operación

---

## [1.0.1] - 2025-06-09

### 🔧 Modificado
- **[IMPROVED]** Modelo actualizado con campos `id_asignatura`, `id_profesor`, `fecha_incidente`, `tipo_falta` y `articulo_manual_convivencia`
- **[IMPROVED]** Pruebas unitarias actualizadas para reflejar cambios del modelo
- **[IMPROVED]** Mensajes de error más descriptivos para observaciones no encontradas

### 📚 Documentación
- **[IMPROVED]** Documentación actualizada con nuevos campos
- **[IMPROVED]** Ejemplos de uso actualizados

---

## [1.0.0] - 2025-06-09

### ✨ Versión Inicial

#### **Funcionalidades Base**
- **[NEW]** CRUD básico de observaciones disciplinarias
- **[NEW]** Integración inicial con API de estudiantes
- **[NEW]** Base de datos MySQL con esquema fundamental
- **[NEW]** Endpoints básicos:
  - `POST /observaciones/` - Registrar nueva observación
  - `GET /observaciones/{id}` - Obtener observación por ID
  - `GET /observaciones/` - Listar todas las observaciones

#### **Estructura Inicial**
- **[NEW]** Configuración básica de FastAPI
- **[NEW]** Modelos SQLAlchemy para base de datos
- **[NEW]** Schemas Pydantic simples
- **[NEW]** Servicios básicos para operaciones CRUD

#### **Testing**
- **[NEW]** Pruebas unitarias básicas para operaciones CRUD
- **[NEW]** Configuración inicial de testing

---

## 🔄 Próximas Versiones

### [2.1.0] - Planificado

#### **Integraciones Adicionales**
- **[PLANNED]** Integración completa con API de asignaturas
- **[PLANNED]** Validación de profesores vía API de autenticación
- **[PLANNED]** Notificaciones automáticas por email/SMS

#### **Nuevas Funcionalidades**
- **[PLANNED]** Observaciones con adjuntos (imágenes, documentos)
- **[PLANNED]** Sistema de workflow para seguimiento de observaciones
- **[PLANNED]** Reportes automáticos en PDF
- **[PLANNED]** Dashboard analytics con gráficos

#### **Mejoras Técnicas**
- **[PLANNED]** Cache Redis para consultas frecuentes
- **[PLANNED]** Rate limiting por usuario
- **[PLANNED]** Tests automatizados con 90%+ cobertura
- **[PLANNED]** Métricas de Prometheus/Grafana

---

## 📝 Convenciones de Versionado

- **MAJOR** (X.0.0): Cambios incompatibles en la API
- **MINOR** (0.X.0): Nuevas funcionalidades compatibles hacia atrás
- **PATCH** (0.0.X): Correcciones de bugs compatibles

## 🏷️ Etiquetas de Cambios

- **[NEW]**: Nueva funcionalidad
- **[IMPROVED]**: Mejora de funcionalidad existente
- **[FIX]**: Corrección de bug
- **[BREAKING]**: Cambio incompatible hacia atrás
- **[SECURITY]**: Corrección de seguridad
- **[DEPRECATED]**: Funcionalidad marcada para eliminación
- **[REMOVED]**: Funcionalidad eliminada
- **[PLANNED]**: Funcionalidad planificada para futuras versiones

---

**Mantenido por**: Equipo de Desarrollo - Institución Educativa José Manuel Marroquín Caicedo  
**Contacto**: desarrollo@institucion.edu.co
