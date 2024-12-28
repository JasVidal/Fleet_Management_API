from flask import Flask
from database.db import db

#------ Se define el modelo para "tabla taxi" ------
class Taxis(db.Model):
    __tablename__ = 'taxis'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String, nullable=False)

    def convert_to_dictionary(self):
            return {
                'id': self.id,
                'plate': self.plate
            }

#Función filtrado para tabla Taxis
def filtered_taxis(plate, page, limit):

    query = Taxis.query
    if plate:
        query = query.filter(Taxis.plate.ilike(f"%{plate}%")) #ilike = tolower

    taxis = query.paginate(page=page, per_page=limit).items
    return [taxi.convert_to_dictionary() for taxi in taxis]
