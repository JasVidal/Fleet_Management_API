from flask import request, jsonify
from app import app
from services import filtered_taxis, filtered_trajectories



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




#Se crea endpoint y función
# - Usa decorador para indicar el URL
@app.route('/trajectories', methods=['GET'])
def trajectories_list():

    #Se obtienen los parámetros
    taxi_id = request.args.get('taxi_id')
    date = request.args.get('date')
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    #Se consulta el registro
    trajectories_data = filtered_trajectories(taxi_id, date, page, limit)

    return jsonify(trajectories_data)
