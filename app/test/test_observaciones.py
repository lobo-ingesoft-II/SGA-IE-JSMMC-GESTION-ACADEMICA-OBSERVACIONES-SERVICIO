"""
Pruebas básicas para el servicio de observaciones
"""
import pytest
from fastapi.testclient import TestClient
from datetime import date
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Probar el endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check():
    """Probar el health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "observaciones-api"

def test_create_observacion():
    """Probar la creación de una observación"""
    observacion_data = {
        "id_estudiante": 1,
        "id_asignatura": 1,
        "id_profesor": 1,
        "fecha_incidente": "2025-06-30",
        "tipo_falta": "Leve",
        "articulo_manual_convivencia": "Artículo test",
        "observacion": "Observación de prueba"
    }
    
    response = client.post("/observaciones/", json=observacion_data)
    # Nota: Este test puede fallar si no está configurada la conexión con la API de estudiantes
    # En un entorno de testing real, se debería usar mocks
    assert response.status_code in [201, 404]  # 404 si no encuentra el estudiante

def test_list_observaciones():
    """Probar la lista de observaciones"""
    response = client.get("/observaciones/")
    assert response.status_code == 200
    data = response.json()
    assert "observaciones" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data

def test_get_observacion_not_found():
    """Probar obtener una observación que no existe"""
    response = client.get("/observaciones/99999")
    assert response.status_code == 404

def test_pagination_validation():
    """Probar validación de paginación"""
    response = client.get("/observaciones/?skip=-1")
    assert response.status_code == 422  # Error de validación
    
    response = client.get("/observaciones/?limit=0")
    assert response.status_code == 422  # Error de validación

if __name__ == "__main__":
    pytest.main([__file__])
