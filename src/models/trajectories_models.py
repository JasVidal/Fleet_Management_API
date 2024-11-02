from flask import Flask
from database.db import db
from sqlalchemy import String, func
from models.taxis_models import Taxis
from datetime import datetime

#------ Se define el modelo para "tabla trajectories" ------
class Trajectories(db.Model):
    __tablename__ = 'trajectories'
    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer, db.ForeignKey('taxis.id'))
    date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def convert_to_dictionary(self):
        return {
            'id': self.id,
            'taxiId': self.taxi_id,
            'date': self.date,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
        
    #Función latest
    def latest_trajectories_list():

        subquery = db.session.query(
        Trajectories.taxi_id,
        func.max(Trajectories.date).label('latest_date')
        ).group_by(Trajectories.taxi_id).subquery()

        latest_trajectories = db.session.query(
            Taxis.id,
            Taxis.plate,
            Trajectories.taxi_id,
            Trajectories.date,
            Trajectories.latitude,
            Trajectories.longitude,
        ).join(
            Trajectories,
            (Taxis.id == Trajectories.taxi_id)        
        ).join(
            subquery,
            (Trajectories.taxi_id == subquery.c.taxi_id) & (Trajectories.date == subquery.c.latest_date)
        ).all()

        latest_dictionary = [
            {
                'id': row.id,
                'plate': row.plate,
                'taxiId': row.taxi_id,
                'timestamp': row.date.strftime('&Y-%m-%d %H:%M:%S'),
                'latitude': row.latitude,
                'longitude': row.longitude
            }
            for row in latest_trajectories
        ]

        return latest_dictionary

#Función filtrado para tabla Trajectories
def filtered_trajectories(taxi_id, date_string):

    query = db.session.query(Trajectories)

    #Se convierte la fecha de str a datetime
    try:
        date = datetime.strptime(date_string, '%d-%m-%Y')
    except ValueError:
        return None, 'El formato de fecha no es válida. Se necesita el formato DD-MM-YYYY'

    query_trajectories = query.filter( 
        Trajectories.taxi_id == taxi_id, 
        func.date(Trajectories.date) == date.date()
        ).all()

    return [trajectory.convert_to_dictionary() for trajectory in query_trajectories], None
