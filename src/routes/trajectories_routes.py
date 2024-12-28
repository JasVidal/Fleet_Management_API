from flask import Flask, request, jsonify
from models.trajectories_models import filtered_trajectories, Trajectories
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def init_routes_trajectories(app):
    #Se crea endpoint y función
    # - Usa decorador para indicar el URL
    @app.route('/trajectories', methods=['GET'])
    def trajectories_list():

        #Se obtienen los parámetros
        taxi_id = request.args.get('taxiId')
        date = request.args.get('date')

        #Se valida taxi_id
        if not taxi_id:
            return jsonify({'error': 'El taxi_id es requerido'}), 400

         #Se puede eliminar
        if taxi_id:
            try:
                taxi_id = int(taxi_id)
            except ValueError:
                return jsonify({'error': 'El taxi_id debe ser un número'}), 400

        #Se valida date
        if not date:
            return jsonify({'error': 'La fecha es requerida'}), 400

        trajectories_data, error_message = filtered_trajectories(taxi_id, date)

        if error_message:
           return jsonify({"error": error_message}), 400
        
        if not trajectories_data:
            return jsonify({'error': 'No se encontró el ID del taxi'}), 404

        return jsonify(trajectories_data), 200


    @app.route('/trajectories/latest', methods=['GET'])
    def get_latest_trajectory():           
        last_trajectory = Trajectories.latest_trajectories_list()

        return jsonify(last_trajectory)

"""         if not last_trajectory:
            return jsonify({'error': 'No hay trayectorias disponibles'}),404
 """
            

