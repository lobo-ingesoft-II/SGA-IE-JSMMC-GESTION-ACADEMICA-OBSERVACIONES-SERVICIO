# Servicio de Observaciones

## Descripción

Este servicio permite gestionar las observaciones realizadas sobre los estudiantes en el sistema académico. Proporciona funcionalidades para crear, obtener y listar observaciones, facilitando el seguimiento académico.

## Endpoints

### Registrar una observación

**POST** `/observaciones/`

#### Request Body

```json
{
  "id_estudiante": 1,
  "id_asignatura": 1,
  "id_profesor": 1,
  "fecha_incidente": "2025-06-08",
  "tipo_falta": "Falta grave",
  "articulo_manual_convivencia": "Artículo 5, sección 2",
  "observacion": "El estudiante no asistió al evento obligatorio."
}
```

#### Response

**Status:** 200 OK

```json
{
  "id_observacion": 1,
  "id_estudiante": 1,
  "id_asignatura": 1,
  "id_profesor": 1,
  "fecha_incidente": "2025-06-08",
  "tipo_falta": "Falta grave",
  "articulo_manual_convivencia": "Artículo 5, sección 2",
  "observacion": "El estudiante no asistió al evento obligatorio.",
  "fecha_registro": "2025-06-09T12:00:00"
}
```

### Obtener una observación por ID

**GET** `/observaciones/{id_observacion}`

#### Response

**Status:** 200 OK

```json
{
  "id_observacion": 1,
  "id_estudiante": 1,
  "id_asignatura": 1,
  "id_profesor": 1,
  "fecha_incidente": "2025-06-08",
  "tipo_falta": "Falta grave",
  "articulo_manual_convivencia": "Artículo 5, sección 2",
  "observacion": "El estudiante no asistió al evento obligatorio.",
  "fecha_registro": "2025-06-09T12:00:00"
}
```

**Status:** 404 Not Found

```json
{
  "detail": "Observacion not found"
}
```

### Listar todas las observaciones

**GET** `/observaciones/`

#### Response

**Status:** 200 OK

```json
[
  {
    "id_observacion": 1,
    "id_estudiante": 1,
    "id_asignatura": 1,
    "id_profesor": 1,
    "fecha_incidente": "2025-06-08",
    "tipo_falta": "Falta grave",
    "articulo_manual_convivencia": "Artículo 5, sección 2",
    "observacion": "El estudiante no asistió al evento obligatorio.",
    "fecha_registro": "2025-06-09T12:00:00"
  },
  {
    "id_observacion": 2,
    "id_estudiante": 2,
    "id_asignatura": 2,
    "id_profesor": 2,
    "fecha_incidente": "2025-06-09",
    "tipo_falta": "Falta leve",
    "articulo_manual_convivencia": null,
    "observacion": "El estudiante entregó la tarea fuera del tiempo establecido.",
    "fecha_registro": "2025-06-09T12:30:00"
  }
]
```

## Instalación

1. Asegúrate de tener el entorno configurado:

   ```bash
   pip install -r requirements.txt
   ```
2. Configura la base de datos en el archivo `.env`:

   ```env
   DATABASE_URL="mysql+pymysql://user:password@host:port/database"
   ```
3. Ejecuta el servidor:

   ```bash
   uvicorn app.main:app --reload --port 8006
   ```

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest app/tests/test_observaciones.py
```

## Dependencias

* **FastAPI**: Framework principal.
* **SQLAlchemy**: ORM para manejar la base de datos.
* **Pytest**: Framework para pruebas unitarias.

## Documentación interactiva

Accede a la documentación Swagger en [http://localhost:8006/docs](http://localhost:8006/docs) o ReDoc en [http://localhost:8006/redoc](http://localhost:8006/redoc).

## Contacto

Para más información, contactar con el