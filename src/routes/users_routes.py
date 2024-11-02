from flask import Flask, request, jsonify
from models.users_models import filtered_users, save_new_user

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
        if not new_user_data or 'name' not in new_user_data or 'email' not in new_user_data or 'password' not in new_user_data or 'role' not in new_user_data:
            return jsonify({'error': 'Completar lo campos requeridos'}), 400

        #Obtener los datos del nuevo usuario
        name = new_user_data.get('name')
        email = new_user_data.get('email')
        password = new_user_data.get('password')
        role = new_user_data.get('role')

        #Guardar el nuevo usuario y obtenerlo
        new_user = save_new_user({
            'name': name,
            'email': email,
            'password': password,
            'role': role
        })

        return jsonify({
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        }),201