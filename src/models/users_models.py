from flask import Flask
from database.db import db
import bcrypt

#------ Se define el modelo para "tabla trajectories" ------
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def convert_to_dictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

def filtered_users(page, limit):
    query = db.session.query(Users)
    users = query.offset((page - 1) * limit).limit(limit).all()
    return [user.convert_to_dictionary() for user in users]

def save_new_user(user_data_dict):

    #Obtener contraseña
    password = user_data_dict['password']

    #Se oculta la contraseña por 1ra vez con bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    #Obtener rol, con user como valor por defecto

    #Crear objeto usuario con contraseña encriptada
    user_data = Users(
        name=user_data_dict['name'],
        email=user_data_dict['email'],
        password=hashed.decode('utf-8'),
        )

    db.session.add(user_data)
    db.session.commit()
    
    return user_data

def existing_email(email):
    return db.session.query(Users).filter_by(email=email).first()




