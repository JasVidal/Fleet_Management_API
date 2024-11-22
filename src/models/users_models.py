from flask import Flask
from database.db import db
import bcrypt
from models.errors.existing_user_error import InvalidPageError, InvalidLimitError, ExistingEmailError, UncompleteFieldsError, UserNotFoundError, NoModifyError, UserNotExistError


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


#------ Función para obtener Usuarios | endpoint GET ------

def filtered_users(page, limit):
    #Validación de parámetros page y limit
    if not page or page <= 0:
        raise InvalidPageError('Página inválida')
                
    if not limit or limit <=0:
        raise InvalidLimitError({'error': 'Límite inválido'})

    #Consulta a base de datos luego de pasar la validación
    query = db.session.query(Users)
    users = query.offset((page - 1) * limit).limit(limit).all()
    return [user.convert_to_dictionary() for user in users]


#------ Función para guardar nuevo Usuarios | endpoint POST ------

#Validar si existe el email en la base de datos
def existing_email(email):
    return db.session.query(Users).filter_by(email=email).first()


#Función para guardar nuevo Usuarios
def save_new_user(user_data_dict):

    #Validar que se reciben los datos
    if not user_data_dict or 'name' not in user_data_dict or 'password' not in user_data_dict:
        raise UncompleteFieldsError('Completar lo campos requeridos')
    
    #Validar si existe el email en la base de datos
    email = user_data_dict['email']

    if existing_email(email):
        raise ExistingEmailError('Este correo ya existe en el sistema')

    #Obtener contraseña
    password = user_data_dict['password']

    #Se oculta la contraseña por 1ra vez con bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    #Crear objeto usuario con contraseña encriptada
    user_data = Users(
        name=user_data_dict['name'],
        email=user_data_dict['email'],
        password=hashed.decode('utf-8'),
        )

    db.session.add(user_data)
    db.session.commit()
    
    return user_data


#------ Función para actualizar Usuarios | endpoint PATCH ------

def data_to_update(uid, data_update):
    
    user_changed = db.session.query(Users).filter_by(id=uid).first()

    if not user_changed:
        raise UserNotFoundError('No se encuentra el usuario')

    if 'email' in data_update or 'password' in data_update:
            raise NoModifyError('No se puede modificar el email o la contraseña')

    if 'name' in data_update:
        user_changed.name = data_update['name']

    db.session.commit()

    return {
            'message': 'Usuario actualizado correctamente',
            'id': user_changed.id,
            'name':user_changed.name,
            'email': user_changed.email,
        }


#------ Función para borrar Usuarios | endpoint DELETE ------

def delete_by_id_or_email(uid):
    # Buscar al usuario por ID o email
    current_user = None
    
    #Buscar por ID
    current_user = db.session.query(Users).filter_by(id=uid).first()
    
    #Si no se encuentra, buscar por email
    if not current_user:
        current_user = db.session.query(Users).filter_by(email=uid).first()

    if current_user:
        # Eliminar al usuario
        db.session.delete(current_user)  
        db.session.commit()  # Confirmar los cambios
        return current_user  # Retornar el usuario eliminado

    else:
        raise UserNotExistError('Este usuario no existe')

