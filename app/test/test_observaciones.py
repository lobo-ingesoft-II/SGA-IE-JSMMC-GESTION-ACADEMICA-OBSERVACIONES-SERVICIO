from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_observacion():
    response = client.post("/observaciones/", json={
        "id_estudiante": 1,
        "id_asignatura": 1,
        "id_profesor": 1,
        "fecha_incidente": "2025-06-08",
        "tipo_falta": "Falta grave",
        "articulo_manual_convivencia": "Artículo 5, sección 2",
        "observacion": "El estudiante no asistió al evento obligatorio."
    })
    assert response.status_code == 200
    assert response.json()["tipo_falta"] == "Falta grave"

def test_get_observacion():
    response = client.get("/observaciones/1")
    assert response.status_code == 200
    assert "observacion" in response.json()

def test_list_observaciones():
    response = client.get("/observaciones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
