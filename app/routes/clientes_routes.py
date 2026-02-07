from flask import Blueprint, request, jsonify
from ..services.clientes_service import ClientesService
from ..utils.error_handler import AppError

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['POST'])
def create_client():
    """
    Endpoint para crear un nuevo cliente.
    Espera un cuerpo JSON con 'name' y 'email'.
    """
    data = request.get_json()
    if not data:
        raise AppError("No se proporcionaron datos", 400)
    
    # Validación básica
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            raise AppError(f"Falta el campo requerido: {field}", 400)
            
    result = ClientesService.create_client(data)
    return jsonify(result), 201

@clientes_bp.route('/clientes/<client_id>', methods=['GET'])
def get_client(client_id):
    """
    Endpoint para recuperar un cliente por ID.
    Devuelve JSON con 'id', 'name', 'email'.
    """
    result = ClientesService.get_client(client_id)
    return jsonify(result), 200

@clientes_bp.route('/clientes/<client_id>', methods=['PUT'])
def update_client(client_id):
    """
    Endpoint para actualizar un cliente por ID.
    Espera un cuerpo JSON con los campos a actualizar.
    """
    data = request.get_json()
    if not data:
        raise AppError("No se proporcionaron datos", 400)

    result = ClientesService.update_client(client_id, data)
    return jsonify(result), 200
