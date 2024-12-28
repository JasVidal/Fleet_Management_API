from dotenv import load_dotenv
import os #interactua con sistema operativo

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False