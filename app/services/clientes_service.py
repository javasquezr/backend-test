import requests
from flask import current_app
from ..utils.error_handler import AppError

class ClientesService:
    @staticmethod
    def _get_headers():
        # A prueba de futuro: si se necesita un token, añadirlo aquí
        return {"Content-Type": "application/json"}

    @staticmethod
    def _build_url(client_id=None):
        """
        Construye la URL completa para la API externa.
        Maneja correctamente las barras (slashes) al final de la URL base.
        """
        base_url = current_app.config['EXTERNAL_API_URL']
        if not base_url.endswith('/'):
            base_url += '/'
        
        if client_id:
            return f"{base_url}{client_id}"
        return base_url.rstrip('/')

    @staticmethod
    def create_client(data):
        """
        Crea un nuevo cliente enviando una petición POST a la API externa.
        
        Args:
            data (dict): Datos del cliente que contienen 'name' y 'email'.
            
        Returns:
            dict: La respuesta de la API externa (típicamente el cliente creado).
            
        Raises:
            AppError: Si falla la validación (400), la API externa está caída (503) o devuelve un error (502).
        """
        url = ClientesService._build_url()
        try:
            response = requests.post(url, json=data, headers=ClientesService._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
             # Si la API externa devuelve un error, podríamos querer pasarlo o envolverlo
             if response.status_code == 400:
                  raise AppError("Error de validación de la API externa", 400, response.json())
             raise AppError(f"Error de la API externa: {str(e)}", 502)
        except requests.exceptions.RequestException as e:
            raise AppError(f"Error de conexión: {str(e)}", 503)

    @staticmethod
    def get_client(client_id):
        """
        Recupera un cliente por ID desde la API externa.
        
        Args:
            client_id (str): El ID del cliente a recuperar.
            
        Returns:
            dict: Un diccionario con 'id', 'name' y 'email' del cliente.
            
        Raises:
            AppError: Si no se encuentra el cliente (404), error de la API externa (502) o error de conexión (503).
        """
        url = ClientesService._build_url(client_id)
        
        try:
            response = requests.get(url, headers=ClientesService._get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()
            # Transformar respuesta según requerimientos: solo id, name, email
            return {
                "id": data.get("id"),
                "name": data.get("name"),
                "email": data.get("email")
            }
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                 raise AppError("Cliente no encontrado", 404)
            raise AppError(f"Error de la API externa: {str(e)}", 502)
        except requests.exceptions.RequestException as e:
            raise AppError(f"Error de conexión: {str(e)}", 503)

    @staticmethod
    def update_client(client_id, data):
        """
        Actualiza un cliente existente enviando una petición PUT a la API externa.
        
        Args:
            client_id (str): El ID del cliente a actualizar.
            data (dict): Los datos a actualizar.
            
        Returns:
            dict: La respuesta de la API externa.
            
        Raises:
            AppError: Si no se encuentra el cliente (404), error de la API externa (502) o error de conexión (503).
        """
        url = ClientesService._build_url(client_id)

        try:
            response = requests.put(url, json=data, headers=ClientesService._get_headers(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
             if response.status_code == 404:
                 raise AppError("Cliente no encontrado", 404)
             raise AppError(f"Error de la API externa: {str(e)}", 502)
        except requests.exceptions.RequestException as e:
            raise AppError(f"Error de conexión: {str(e)}", 503)
