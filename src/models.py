from app import db

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


#------ Se define el modelo para "tabla trajectories" ------
class Trajectories(db.Model):
    __tablename__ = 'trajectories'
    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def convert_to_dictionary(self):
        return {
            'id': self.id,
            'taxi_id': self.taxi_id,
            'date': self.date,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
