from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database.config import Config
from routes.taxis_routes import *
from routes.trajectories_routes import *
from routes.users_routes import *
from database.db import db



#Se inicia la app Flask y SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)


#Se inicializa SQLAlchemy
db.init_app(app)

init_routes_taxis(app)
init_routes_trajectories(app)
init_routes_users(app)


#Se importan las rutas


if __name__ == '__main__':
    app.run(debug=True)