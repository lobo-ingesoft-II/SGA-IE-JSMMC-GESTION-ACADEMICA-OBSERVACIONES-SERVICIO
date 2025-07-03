# 🎓 API de Observaciones Disciplinarias

API REST para gestión de observaciones disciplinarias de estudiantes.

## 🚀 Inicio Rápido

### Instalación
```bash
# 1. Clonar y navegar al directorio
git clone <repository-url>
cd SGA-IE-JSMMC-GESTION-ACADEMICA-OBSERVACIONES-SERVICIO

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu configuración de base de datos

# 5. Ejecutar servidor
uvicorn app.main:app --reload --port 8003
```

### Acceso
- **API**: http://localhost:8003
- **Documentación**: http://localhost:8003/docs
- **Health Check**: http://localhost:8003/health

## 📚 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/observaciones/` | Listar observaciones (paginado) |
| POST | `/observaciones/` | Crear nueva observación |
| GET | `/observaciones/{id}` | Obtener observación específica |
| PUT | `/observaciones/{id}` | Actualizar observación |
| DELETE | `/observaciones/{id}` | Eliminar observación |
| GET | `/observaciones/estudiante/{id}` | Observaciones por estudiante |

## 💡 Ejemplo de Uso

### Crear Observación
```bash
curl -X POST "http://localhost:8003/observaciones/" \
  -H "Content-Type: application/json" \
  -d '{
    "id_estudiante": 1,
    "id_asignatura": 1,
    "id_profesor": 1,
    "fecha_incidente": "2025-07-02",
    "tipo_falta": "Leve",
    "articulo_manual_convivencia": "Art. 10.1",
    "observacion": "Descripción de la observación"
  }'
```

### Integración Frontend (JavaScript)
```javascript
const API_BASE_URL = 'http://localhost:8003';

// Listar observaciones
async function getObservaciones(skip = 0, limit = 50) {
  const response = await fetch(`${API_BASE_URL}/observaciones/?skip=${skip}&limit=${limit}`);
  return await response.json();
}

// Crear observación
async function createObservacion(data) {
  const response = await fetch(`${API_BASE_URL}/observaciones/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return await response.json();
}

// Tipos de falta manejados por el frontend
const TIPOS_FALTA = ['Leve', 'Grave', 'Gravísima'];
```

## ⚙️ Configuración

### Variables de Entorno (.env)
```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=observaciones_db

# APIs externas
ESTUDIANTES_API_URL=http://localhost:8005
```

### Estructura de Datos
```json
{
  "id_estudiante": 1,
  "id_asignatura": 1,
  "id_profesor": 1,
  "fecha_incidente": "2025-07-02",
  "tipo_falta": "Leve|Grave|Gravísima",
  "articulo_manual_convivencia": "Art. 10.1",
  "observacion": "Descripción mínima de 10 caracteres"
}
```

## 🚀 Producción

```bash
# Ejecutar en producción con Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8003 --workers 4

# O con configuración adicional para producción
uvicorn app.main:app --host 0.0.0.0 --port 8003 --workers 4 --log-level warning
```

## 📝 Notas Importantes

- **Campo tipo_falta**: Acepta cualquier string, el frontend debe manejar las opciones
- **✅ Validación de estudiantes**: SÍ se integra con la API de estudiantes (puerto 8005)
- **Paginación**: Límite máximo de 100 registros por consulta
- **CORS**: Configurado para desarrollo local (puertos 3000, 5173, 8080)
- **Dependencia**: Requiere que la API de estudiantes esté ejecutándose en el puerto 8005

## 🛠️ Tecnologías

- **FastAPI** 0.104+
- **SQLAlchemy** 2.0+
- **MySQL** 8.0+
- **Python** 3.8+

---

**Puerto**: 8003 | **Documentación**: `/docs` | **Health Check**: `/health`
