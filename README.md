# Backend Test – Python Flask API Integration

## Descripción
Este proyecto implementa un microservicio backend en **Python y Flask** que actúa como intermediario entre un sistema interno y una **API externa**, permitiendo crear, consultar y actualizar clientes mediante endpoints REST.

---

## Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone <repositorio>
cd backend-test
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

> **Nota para Windows:** Si el comando `python` no funciona, intenta usar `py` (el lanzador de Python):
> ```bash
> py -m venv venv
> ```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto:
```env
EXTERNAL_API_URL=https://api-externa.com/clientes
FLASK_ENV=development
```

### 5. Ejecutar la aplicación
```bash
python app/app.py
```

---

## Estructura del proyecto

```
backend-test/
│
├── app/
│   ├── app.py
│   ├── config.py
│   ├── routes/
│   │   └── clientes_routes.py
│   ├── services/
│   │   └── clientes_service.py
│   └── utils/
│       └── error_handler.py
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

### Descripción de carpetas
- **app.py**: Punto de entrada de la aplicación Flask.
- **config.py**: Carga y gestión de variables de entorno.
- **routes/**: Definición de endpoints y manejo de solicitudes HTTP.
- **services/**: Lógica de negocio y consumo de la API externa.
- **utils/**: Manejo centralizado de errores y utilidades comunes.

---

## Endpoints disponibles

### POST /clientes
- Recibe datos en formato JSON.
- Valida campos obligatorios: `name`, `email`.
- Envía la información a la API externa.
- Retorna la respuesta o un error controlado.

### GET /clientes/<id>
- Consulta un cliente en la API externa.
- Transforma la respuesta.
- Retorna únicamente:
  - `id`
  - `name`
  - `email`

### PUT /clientes/<id>
- Recibe datos en formato JSON.
- Envía la actualización a la API externa.
- Retorna el resultado de la operación.
- Maneja errores si la API externa falla.

---

## Manejo de errores
El sistema maneja los errores de la siguiente manera:
- **Errores de validación** → HTTP 400
- **Errores de conexión con API externa** → HTTP 503
- **Respuestas no exitosas de la API externa** → HTTP 502
- **Errores inesperados** → HTTP 500

El manejo de errores está centralizado para mejorar mantenibilidad y claridad. Además, **todos los mensajes de error se devuelven en español**.

---

## Respuestas a Preguntas Técnicas

### 5. ¿Qué cambios realizaría si la API externa requiriera autenticación Bearer Token?
Si la API externa requiriera autenticación mediante Bearer Token, realizaría los siguientes cambios:

1.  **Configuración**: Agregar la variable `EXTERNAL_API_TOKEN` en el archivo `.env` y cargarla en `config.py`.
2.  **Servicio**: Modificar el método `_get_headers` en `ClientesService` para incluir el encabezado de autorización:
    ```python
    @staticmethod
    def _get_headers():
        token = current_app.config.get('EXTERNAL_API_TOKEN')
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    ```
Esto asegura que el token se envíe automáticamente en todas las peticiones sin modificar cada método individualmente.

### 6. ¿Qué mejoras implementaría en un entorno productivo?
Para llevar este microservicio a un entorno de producción, implementaría las siguientes mejoras:

-   **Servidor de Aplicaciones**: Utilizar un servidor WSGI robusto como **Gunicorn** o **uWSGI** en lugar del servidor de desarrollo de Flask (`werkzeug`), detrás de un servidor web como Nginx.
-   **Dockerización**: Crear un `Dockerfile` y un `docker-compose.yml` para garantizar la consistencia entre entornos y facilitar el despliegue.
-   **Logging Estructurado**: Implementar una configuración de logging avanzada (ej. JSON logs) que se integre con sistemas de monitoreo (ELK Stack, Datadog) en lugar de usar `print`.
-   **CI/CD**: Configurar pipelines de Integración y Despliegue Continuo (GitHub Actions, GitLab CI) para ejecutar tests automáticos y linter antes de cada despliegue.
-   **Gestión de Secretos**: Utilizar servicios de gestión de secretos (AWS Secrets Manager, HashiCorp Vault) en lugar de archivos `.env` en producción.
-   **Monitoreo y Métricas**: Integrar herramientas como Prometheus y Grafana para monitorear la salud del servicio, latencia y tasas de error en tiempo real.

---

## Implementación Actual

### Requisitos Previos
- Python 3.8+
- git

### Ejecución de Pruebas (Tests)
El proyecto incluye tests unitarios con **pytest** que mockean la API externa para verificar la lógica de negocio sin conexión a internet.

1. Instalar dependencias de desarrollo:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar los tests:
   ```bash
    pytest tests/ -v
   ```

### Decisiones de Diseño
- **Arquitectura en Capas**: Se separó la lógica en `routes`, `services` y `utils` para mantener `app.py` limpio.
- **Manejo de Errores Centralizado**: `AppError` en `utils/error_handler.py` permite lanzar excepciones controladas desde cualquier lugar del código que se traducen automáticamente a respuestas JSON consistentes.
- **Configuración**: Uso de `python-dotenv` para cargar variables de entorno desde `.env`.
- **Testing con Mocks**: Se utiliza `unittest.mock` para simular las respuestas de la API externa, asegurando que los tests sean rápidos y deterministas.
- **Localización**: Todo el código, comentarios y mensajes de error han sido traducidos al español para facilitar el mantenimiento por equipos hispanohablantes.

---

## Uso de la Colección de Postman

El proyecto incluye un archivo `Backend_Test_Postman_Collection.json` listo para probar los endpoints.

1.  **Abrir Postman**: Asegúrate de tener Postman instalado.
2.  **Importar la Colección**:
    - Ve a `File` > `Import`.
    - Selecciona o arrastra el archivo `Backend_Test_Postman_Collection.json`.
3.  **Ejecutar el Servidor**:
    - Asegúrate de que tu aplicación esté corriendo (`python app/app.py`).
4.  **Probar Endpoints**:
    - La colección incluye ejemplos preconfigurados para `Crear`, `Obtener` y `Actualizar` clientes.
    - Ejecuta las peticiones en orden para verificar el flujo completo.

---

## Entregables
- Código fuente completo
- Archivo README.md (Actualizado)
- Colección de Postman (Ya incluida en repositorio)
- Video explicativo (Pendiente)

