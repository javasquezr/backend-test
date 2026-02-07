import pytest
from unittest.mock import patch, MagicMock
from app.utils.error_handler import AppError

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

@patch('app.services.clientes_service.requests.post')
def test_create_client_success(mock_post, client):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "name": "Test", "email": "test@test.com"}
    mock_post.return_value = mock_response

    payload = {"name": "Test", "email": "test@test.com"}
    response = client.post('/clientes', json=payload)
    
    assert response.status_code == 201
    assert response.json['id'] == 1

@patch('app.services.clientes_service.requests.post')
def test_create_client_validation_error(mock_post, client):
    payload = {"name": "Test"} # Falta email
    response = client.post('/clientes', json=payload)
    
    assert response.status_code == 400
    assert "Falta el campo requerido" in response.json['message']

@patch('app.services.clientes_service.requests.get')
def test_get_client_success(mock_get, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    # La API externa podría devolver más datos, solo queremos id, name, email
    mock_response.json.return_value = {
        "id": 1, 
        "name": "Test", 
        "email": "test@test.com",
        "extra_field": "ignorar esto"
    }
    mock_get.return_value = mock_response

    response = client.get('/clientes/1')
    
    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "Test", "email": "test@test.com"}
    assert "extra_field" not in response.json

@patch('app.services.clientes_service.requests.get')
def test_get_client_not_found(mock_get, client):
    mock_response = MagicMock()
    mock_response.status_code = 404
    from requests.exceptions import HTTPError
    error = HTTPError()
    error.response = mock_response
    mock_response.raise_for_status.side_effect = error
    
    mock_get.return_value = mock_response

    response = client.get('/clientes/999')
    assert response.status_code == 404
    assert response.json['message'] == "Cliente no encontrado"

@patch('app.services.clientes_service.requests.put')
def test_update_client_success(mock_put, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_put.return_value = mock_response

    payload = {"name": "Updated", "email": "updated@test.com"}
    response = client.put('/clientes/1', json=payload)
    
    assert response.status_code == 200
