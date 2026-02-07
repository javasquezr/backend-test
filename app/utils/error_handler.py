from flask import jsonify

class AppError(Exception):
    def __init__(self, message, status_code, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "Solicitud incorrecta"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"message": "Error interno del servidor"}), 500
