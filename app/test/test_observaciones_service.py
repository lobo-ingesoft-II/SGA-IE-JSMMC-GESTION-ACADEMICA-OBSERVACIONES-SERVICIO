import pytest
from unittest.mock import MagicMock, patch
from datetime import date, datetime
from sqlalchemy.orm import Session

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
    count_observaciones,
    count_observaciones_by_estudiante
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
    return MagicMock(spec=Session)

# TEST para crear observación
def test_create_observacion(mock_db):
    dummy_create = build_dummy_observacion_create()
    dummy_model = build_dummy_observacion_model()
    
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    with patch('app.services.observaciones.Observacion', return_value=dummy_model):
        result = create_observacion(mock_db, dummy_create)
        
        assert result.id_estudiante == 1
        assert result.tipo_falta == "Leve"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

# TEST para obtener observación por ID válido
def test_get_observacion_valid(mock_db):
    dummy_model = build_dummy_observacion_model()
    mock_db.query.return_value.filter.return_value.first.return_value = dummy_model
    
    result = get_observacion(mock_db, 1)
    
    assert result.id_observacion == 1
    assert result.id_estudiante == 1

# TEST para obtener observación por ID no encontrado
def test_get_observacion_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    result = get_observacion(mock_db, 999)
    
    assert result is None

# TEST para listar observaciones
def test_list_observaciones(mock_db):
    dummy_list = [build_dummy_observacion_model()]
    mock_db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = dummy_list
    
    result = list_observaciones(mock_db, skip=0, limit=10)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id_observacion == 1

# TEST para obtener observaciones por estudiante
def test_get_observaciones_by_estudiante(mock_db):
    dummy_list = [build_dummy_observacion_model()]
    mock_db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = dummy_list
    
    result = get_observaciones_by_estudiante(mock_db, 1, skip=0, limit=10)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id_estudiante == 1

# TEST para actualizar observación exitoso
def test_update_observacion_success(mock_db):
    dummy_model = build_dummy_observacion_model()
    dummy_update = ObservacionUpdate(observacion="Observación actualizada")
    
    mock_db.query.return_value.filter.return_value.first.return_value = dummy_model
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    result = update_observacion(mock_db, 1, dummy_update)
    
    assert result is not None
    mock_db.commit.assert_called_once()

# TEST para actualizar observación no encontrada
def test_update_observacion_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    dummy_update = ObservacionUpdate(observacion="Observación actualizada")
    
    result = update_observacion(mock_db, 999, dummy_update)
    
    assert result is None

# TEST para eliminar observación exitoso
def test_delete_observacion_success(mock_db):
    dummy_model = build_dummy_observacion_model()
    mock_db.query.return_value.filter.return_value.first.return_value = dummy_model
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None
    
    result = delete_observacion(mock_db, 1)
    
    assert result is not None
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()

# TEST para eliminar observación no encontrada
def test_delete_observacion_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    result = delete_observacion(mock_db, 999)
    
    assert result is None

# TEST para contar observaciones
def test_count_observaciones(mock_db):
    mock_db.query.return_value.count.return_value = 5
    
    result = count_observaciones(mock_db)
    
    assert result == 5

# TEST para contar observaciones por estudiante
def test_count_observaciones_by_estudiante(mock_db):
    mock_db.query.return_value.filter.return_value.count.return_value = 3
    
    result = count_observaciones_by_estudiante(mock_db, 1)
    
    assert result == 3