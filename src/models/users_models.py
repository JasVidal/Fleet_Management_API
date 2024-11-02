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
    role = db.Column(db.String, nullable=False)

    def convert_to_dictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }

def filtered_users(page, limit):
    query = db.session.query(Users)
    users = query.offset((page - 1) * limit).limit(limit).all()
    return [user.convert_to_dictionary() for user in users]

def save_new_user(user_data_dict):

    password = user_data_dict['password']
    #Se oculta la contraseño por 1ra vez con un random salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    #Revisar que visible password matchea con la anterior oculta

    role=user_data_dict.get('role', 'user')

    user_data = Users(
        name=user_data_dict['name'],
        email=user_data_dict['email'],
        password=hashed.decode('utf-8'),
        role=user_data_dict.get('role')
        )

    db.session.add(user_data)
    db.session.commit()

    return user_data

"""     #Validar si la contraseña es correcta
    if bcrypt.checkpw(password, hashed):
        print('¡Contraseña correcta! :DD')
    else:
        print('Contraseña incorrecta ):') """
    