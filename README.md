# 📚 SGA-IE-JSMMC-OBSERVACIONES-SERVICIO

**Autor:** Javier Esteban Martinez Giron

---
API o Servicio para la gestión de observaciones disciplinarias.

---

## 📝 Descripción general

API para la gestión de observaciones disciplinarias de estudiantes en la Institución Educativa Departamental Josué Manrique.  
Permite registrar, consultar, actualizar y eliminar observaciones disciplinarias, almacenando la información en MySQL y exponiendo endpoints REST documentados con Swagger/FastAPI.

---

## 🎯 Funcionalidades

- Registro y validación de observaciones disciplinarias.
- Consulta de observaciones por ID o listado completo.
- Filtrado de observaciones por estudiante.
- Actualización y eliminación de registros.
- Documentación interactiva con Swagger (FastAPI).
- Observabilidad con Prometheus para monitoreo.

---

## 🔧 Endpoints REST

| Método | Endpoint                           | Descripción                                  |
|--------|------------------------------------|--------------------------------------------- |
| GET    | `/observaciones/`                  | Listar todas las observaciones               |
| GET    | `/observaciones/{id_observacion}`  | Consultar una observación por ID             |
| GET    | `/observaciones/estudiante/{id}`   | Listar observaciones de un estudiante        |
| POST   | `/observaciones/`                  | Crear una nueva observación                  |
| PUT    | `/observaciones/{id_observacion}`  | Actualizar una observación existente         |
| DELETE | `/observaciones/{id_observacion}`  | Eliminar una observación                     |
| GET    | `/observaciones/custom_metrics`    | Obtener métricas de Prometheus               |
---

### 📊 Observabilidad

La API incluye métricas de Prometheus para monitoreo:

```bash
# Ver métricas
curl http://localhost:8011/observaciones/custom_metrics
```

Métricas disponibles:
- Contador de peticiones: `http_requests_total`
- Latencia: `http_request_duration_seconds`
- Errores: `http_request_errors_total`

---

### 📑 Swagger

La documentación Swagger está disponible en:
http://localhost:8011/docs
---

### ⚙️ Configuración !!!IMPORTANTE 
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=observaciones_db
ESTUDIANTES_API_URL=http://localhost:8005
```

---
### 🚀 Instalación y Ejecución
Instala las dependencias:
```bash
pip install -r requirements.txt
```
Ejecuta el servidor:
```bash
uvicorn app.main:app --reload --port 8011
```

---
###  🚀 Correr pruebas unitarias

De forma global 
```bash
pytest
```

De forma más específica
```bash
pytest app/test/test_observaciones_service.py
```

Prueba específica
```bash
pytest app/test/test_observaciones_service.py::test_create_observacion
```

---
### ¿Porque puerto 8011 para el servidor Uvicorn?
Porque se va a llamar ahí para la petición de la api de observaciones.

---
### 🔧 Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|----------|
| **FastAPI** | 0.104+ | Framework web |
| **SQLAlchemy** | 2.0+ | ORM |
| **MySQL** | 8.0+ | Base de datos |
| **Pydantic** | 2.0+ | Validación |
| **Prometheus Client** | 0.19+ | Métricas |
| **Pytest** | 7.0+ | Testing |
| **Python** | 3.8+ | Lenguaje |