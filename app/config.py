import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "https://api-externa.com/clientes")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = FLASK_ENV == "development"
