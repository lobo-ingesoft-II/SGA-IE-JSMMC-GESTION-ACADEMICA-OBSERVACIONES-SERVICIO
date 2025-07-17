import pytest
from unittest.mock import MagicMock, patch
from datetime import date, datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.schemas.observaciones import ObservacionCreate, ObservacionUpdate
from app.models.observaciones import Observacion
from app.services.observaciones import (
    create_observacion,
    get_observacion,
    list_observaciones,
    get_observaciones_by_estudiante,
    update_observacion,
    delete_observacion,
    count_observaciones
)

def build_dummy_observacion_create():
    return ObservacionCreate(
        id_estudiante=1,
        id_asignatura=1,
        id_profesor=1,
        fecha_incidente=date(2024, 1, 15),
        tipo_falta="Leve",
        articulo_manual_convivencia="Art. 15",
        observacion="El estudiante llegó tarde a clase sin justificación válida"
    )

def build_dummy_observacion_model():
    return Observacion(
        id_observacion=1,
        id_estudiante=1,
        id_asignatura=1,
        id_profesor=1,
        fecha_incidente=date(2024, 1, 15),
        tipo_falta="Leve",
        articulo_manual_convivencia="Art. 15",
        observacion="El estudiante llegó tarde a clase sin justificación válida",
        fecha_registro=datetime(2024, 1, 15, 10, 30, 0)
    )

@pytest.fixture
def mock_db():
    return MagicMock()

# TEST básicos de servicios
def test_create_observacion_service(mock_db):
    dummy_create = build_dummy_observacion_create()
    dummy_model = build_dummy_observacion_model()
    
    with patch('app.services.observaciones.Observacion', return_value=dummy_model):
        result = create_observacion(mock_db, dummy_create)
        assert result.id_estudiante == 1
        assert result.tipo_falta == "Leve"

def test_get_observacion_found(mock_db):
    dummy_model = build_dummy_observacion_model()
    mock_db.query.return_value.filter.return_value.first.return_value = dummy_model
    
    result = get_observacion(mock_db, 1)
    assert result.id_observacion == 1

def test_get_observacion_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    result = get_observacion(mock_db, 999)
    assert result is None

def test_list_observaciones_service(mock_db):
    dummy_list = [build_dummy_observacion_model()]
    mock_db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = dummy_list
    
    result = list_observaciones(mock_db, skip=0, limit=10)
    assert isinstance(result, list)
    assert len(result) == 1

def test_count_observaciones_service(mock_db):
    mock_db.query.return_value.count.return_value = 5
    
    result = count_observaciones(mock_db)
    assert result == 5

def test_update_observacion_success(mock_db):
    dummy_model = build_dummy_observacion_model()
    dummy_update = ObservacionUpdate(observacion="Observación actualizada")
    
    mock_db.query.return_value.filter.return_value.first.return_value = dummy_model
    
    result = update_observacion(mock_db, 1, dummy_update)
    assert result is not None

def test_delete_observacion_success(mock_db):
    dummy_model = build_dummy_observacion_model()
    mock_db.query.return_value.filter.return_value.first.return_value = dummy_model
    
    result = delete_observacion(mock_db, 1)
    assert result is not None

# TEST de métricas endpoint
def test_custom_metrics_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/observaciones/custom_metrics")
    
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]