from flask import Flask, request, jsonify
#from app import app
from models.taxis_models import filtered_taxis

def init_routes_taxis(app):
    #Se crea endpoint y función
    # - Usa decorador para indicar el URL
    @app.route('/taxis', methods=['GET'])
    def taxis_list():

        #Se establecen los parámetros
        plate = request.args.get('plate')
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)

        #Se llama a la función
        taxis_data = filtered_taxis(plate, page, limit)

        return jsonify(taxis_data)
