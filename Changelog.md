# Changelog - Servicio de Observaciones

## [1.0.0] - 2025-06-09
### Agregado
- Creación del servicio de observaciones.
- Endpoint **POST** `/observaciones/` para registrar una nueva observación.
- Endpoint **GET** `/observaciones/{id_observacion}` para obtener una observación por ID.
- Endpoint **GET** `/observaciones/` para listar todas las observaciones.
- Integración de modelos, esquemas y servicios con SQLAlchemy y Pydantic.
- Pruebas unitarias básicas para las operaciones CRUD de observaciones.

## [1.0.1] - 2025-06-09
### Modificado
- Ajuste en el modelo para incluir los campos `id_asignatura`, `id_profesor`, `fecha_incidente`, `tipo_falta` y `articulo_manual_convivencia`.
- Actualización de las pruebas unitarias y documentación para reflejar los cambios.
- Mejoras en los mensajes de error para observaciones no encontradas.
