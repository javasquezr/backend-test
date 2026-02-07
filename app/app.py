from flask import Flask
from .config import Config
from .routes.clientes_routes import clientes_bp
from .utils.error_handler import register_error_handlers, AppError

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_error_handlers(app)
    
    app.register_blueprint(clientes_bp)
    
    @app.route('/health')
    def health_check():
        return {"status": "ok"}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
