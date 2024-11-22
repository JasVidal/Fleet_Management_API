from flask import Flask, request, jsonify
from models.users_models import filtered_users, save_new_user,existing_email, data_to_update, delete_by_id_or_email
from models.errors.existing_user_error import InvalidPageError, InvalidLimitError, ExistingEmailError, UncompleteFieldsError, UserNotFoundError, NoModifyError, EmptyRequestError, UserNotExistError

def init_routes_users(app):

#------ Endpoint para OBTENER Usuarios con método GET ------

    @app.route('/users', methods=['GET'])
    def users_list():

        #Se establecen los parámetros
        page = request.args.get('page', default=1)
        limit = request.args.get('limit', default=10)
        
        try:
            page = int(page)
            limit = int(limit)
            
            #Se llama a la función
            users = filtered_users(page, limit)

            return jsonify(users)

        except ValueError:
            return jsonify({'error': 'Los parámetros no son válidos'}), 400

        except InvalidPageError as error:
            return jsonify({'error': error.value}), 400
        
        except InvalidLimitError as error:
            return jsonify({'error': error.value}), 400


#------ Endpoint para CREAR Usuarios con método POST ------

    @app.route('/users', methods=['POST']) #save info
    def create_user(): #especificar la info a guardar
        
        try:
            
            new_user_data = request.get_json()

            # Llamar a la función save_new_user que ahora realiza la validación y creación del usuario
            new_user = save_new_user(new_user_data)

            return jsonify({
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email,
            }), 201
        
        except ExistingEmailError as error: 
            return jsonify({'error': error.value}), 409

        except UncompleteFieldsError as error:
            return jsonify({'error': error.value}), 400


#------ Endpoint para ACTUALIZAR Usuarios con método PATCH ------

    @app.route('/users/<int:uid>', methods=['PATCH']) #actualizar info

    def update_user(uid):

        data_update = request.get_json()

        if data_update is None:
            raise EmptyRequestError('El cuerpo de la solicitud está vacío')
        
        # Llamamos a data_to_update para realizar la lógica de la actualización
        try:
            # Si todo está bien, procedemos a actualizar
            new_data = data_to_update(uid, data_update)
            return jsonify(new_data), 200

        except EmptyRequestError as error:
            # Si ocurre un ValueError: cuerpo vacío
            return jsonify({'error': error.value}), 400

        except NoModifyError as error:
            # Si hay errores como intento de modificar email o password
            return jsonify({'error': error.value}), 400

        except UserNotFoundError as error:
            # Si el usuario no existe
            return jsonify({'error': error.value}), 404

#------ Endpoint para BORRAR Usuarios con método DELETE ------

    @app.route('/users/<uid>', methods=['DELETE'])
    
    def delete_user(uid):
        
        try:
            user_to_delete = delete_by_id_or_email(uid) 

            return jsonify({
            'id': user_to_delete.id,
            'email': user_to_delete.email,
            'name': user_to_delete.name
            }), 200

        # Si el usuario no se encuentra, devolver un error 404
        except UserNotExistError as error:
            return jsonify({'error': error.value}), 404