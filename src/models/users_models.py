from flask import Flask, request, jsonify
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

#--------SEPARACION------------

def data_to_update(uid):
    
    user_changed = db.session.query(Users).filter_by(id=uid).first()

    if not user_changed:
        return jsonify({'error': 'El usuario no existe jeje'}), 404

    data_update = request.get_json()

    if data_update is None:
        return jsonify({'error': 'El cuerpo de la solicitud está vacío'}), 400

    if 'email' in data_update or 'password' in data_update:
            return jsonify({'error': 'No se puede modificar el email o la contraseña'}), 400

    if 'name' in data_update:
        user_changed.name = data_update['name']

    db.session.commit()

    return jsonify({
            'message': 'Usuario actualizado correctamente',
            'id': user_changed.id,
            'name':user_changed.name,
            'email': user_changed.email,
        }), 200

#--------------------------------------------

def delete_by_id_or_email(uid):
    # Buscar al usuario por ID o email
    current_user = None
    
    if isinstance(uid, str):
        current_user = db.session.query(Users).filter_by(email=uid).first()
    
    else:
        current_user = db.session.query(Users).filter_by(id=uid).first()

    if current_user:
        db.session.delete(current_user)  # Eliminar al usuario
        db.session.commit()  # Confirmar los cambios
        return current_user  # Si el usuario fue eliminado, retornar el usuario
    return None

