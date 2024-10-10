from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

#Se inicia la app Flask y SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)


#Se inicializa SQLAlchemy
db = SQLAlchemy(app)

#Se importan las rutas
from routes import *


if __name__ == '__main__':
    app.run(debug=True)