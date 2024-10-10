from models import Taxis, Trajectories

#Función filtrado para tabla Taxis
def filtered_taxis(plate, page, limit):

    query = Taxis.query
    if plate:
        query = query.filter(Taxis.plate.ilike(f"%{plate}%")) #ilike = tolower

    taxis = query.paginate(page=page, per_page=limit).items
    return [taxi.convert_to_dictionary() for taxi in taxis]

#Función filtrado para tabla Trajectories
def filtered_trajectories(taxi_id, date, page, limit):

    query = Trajectories.query

    if taxi_id:
        query = query.filter(Trajectories.taxi_id == taxi_id)

    if date:
        query = query.filter(Trajectories.date.ilike(f"%{date}%"))
    
    trajectories = query.paginate(page=page, per_page=limit).items
    return [trajectory.convert_to_dictionary() for trajectory in trajectories]