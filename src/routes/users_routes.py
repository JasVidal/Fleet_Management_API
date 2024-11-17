from flask import Flask, request, jsonify
from models.users_models import filtered_users, save_new_user,existing_email, data_to_update, delete_by_id_or_email

def init_routes_users(app):
    #Se crea endpoint y función
    # - Usa decorador para indicar el URL
    @app.route('/users', methods=['GET'])
    def users_list():

        #Se establecen los parámetros
        page = request.args.get('page', default=1)
        limit = request.args.get('limit', default=10)
        
        try:
            page = int(page)
            limit = int(limit)

        except ValueError:
            return jsonify({'error': 'Los parámetros no son válidos'}), 400

        if not page or page <= 0:
            return jsonify({'error': 'Página inválida'}), 400
                    
        if not limit or limit <=0:
            return jsonify({'error': 'Límite inválido'}), 400
            
        #Se llama a la función
        users = filtered_users(page, limit)

        return jsonify(users)

    @app.route('/users', methods=['POST']) #save info
    def create_user(): #especificar la info a guardar
        
        new_user_data = request.get_json()

        #Validar que se reciben los datos
        if not new_user_data or 'name' not in new_user_data or 'password' not in new_user_data:
            return jsonify({'error': 'Completar lo campos requeridos'}), 400

        #Obtener los datos del nuevo usuario
        name = new_user_data['name']
        email = new_user_data['email']
        password = new_user_data['password']

        existing_user = existing_email(email)
        if existing_user:
            return jsonify({'error': 'Este correo ya existe en el sistema'}), 409

        #Guardar el nuevo usuario y obtenerlo
        new_user = save_new_user({
            'name': name,
            'email': email,
            'password': password,
        })

        return jsonify({
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email,
        }), 201


    @app.route('/users/<int:uid>', methods=['PATCH']) #actualizar info

    def update_user(uid):

        new_data = data_to_update(uid)
        
        return new_data

        #Verificar que no se intenta cambiar email o password

    @app.route('/users/<uid>', methods=['DELETE'])
    
    def delete_user(uid):
        user_to_delete = delete_by_id_or_email(uid) 

        if not user_to_delete:
            return jsonify({'error': 'Este usuario no existe'}), 404

        return jsonify({
        'id': user_to_delete.id,
        'email': user_to_delete.email,
        'name': user_to_delete.name
    }), 200