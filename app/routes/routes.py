import datetime
import json
import inflect

from flask import Response, jsonify, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.common.common import error_handler
from app.models.animal import Animal
from app.models.center import Center
from app.models.species import Species
from app.models.api_access import Access
from app import file_logger


inflect_engine = inflect.engine()


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    login = request_data['login']
    password = request_data['password']
    Access.add_access_entry(Center.get_center_by_name(login).id, datetime.datetime.utcnow())
    match = Center.password_match(login, password)
    if match:
        token = create_access_token(identity=login)
        return Response(json.dumps({'token': token}), mimetype='application/json')
    else:
        return Response('', 401, mimetype='application/json')


@app.route('/animals', methods=['GET'])
def get_animals():
    return jsonify({'animals': Animal.get_all_animals()})


@app.route('/animals', methods=['POST'])
@jwt_required
@error_handler
def add_animal():
    request_data = request.get_json()
    species = Species.get_species(request_data['species_id'])
    if 'description' not in request_data:
        request_data['description'] = species.description
    if 'price' not in request_data:
        request_data['price'] = species.price
    animal_id = Animal.add_animal(**request_data)
    request_center = get_jwt_identity()
    log_data = {'method_type': request.method, 'req_url': request.path,
                'center_name': request_center,
                'entity_type': 'animal', 'entity_id': animal_id}
    file_logger.info('Animal added', extra=log_data)
    response = Response('', status=201, mimetype='application/json')
    response.headers['Location'] = f'/animals/{animal_id}'
    return response


@app.route('/animals/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    return jsonify(Animal.get_animal(animal_id))


@app.route('/animals/<int:animal_id>', methods=['PUT'])
@jwt_required
@error_handler
def update_animal_info(animal_id):
    request_center = get_jwt_identity()
    log_data = {'method_type': request.method, 'req_url': request.path,
                'center_id': request_center,
                'entity_type': 'animal', 'entity_id': animal_id}
    file_logger.info('Animal replaced', extra=log_data)
    if Center.get_center(Animal.get_animal(animal_id).center_id).login != request_center:
        return Response('Forbidden', status=403)
    request_data = request.get_json()
    species = Species.get_species(request_data['species_id'])
    if 'description' not in request_data:
        request_data['description'] = species.description
    if 'price' not in request_data:
        request_data['price'] = species.price
    Animal.replace_animal(animal_id, **request_data)
    response = Response('', status=204, mimetype='application/json')
    return response


@app.route('/animals/<int:animal_id>', methods=['DELETE'])
@jwt_required
def delete_animal(animal_id):
    request_center = get_jwt_identity()
    log_data = {'method_type': request.method, 'req_url': request.path,
                'center_id': request_center,
                'entity_type': 'animal', 'entity_id': animal_id}
    file_logger.info('Animal deleted', extra=log_data)
    if Center.get_center(Animal.get_animal(animal_id).center_id).login != request_center:
        return Response('Forbidden', status=403)
    if Animal.delete_animal(animal_id):
        return Response('', status=204, mimetype='application/json')
    invalid_animal_msg = {
        'error': 'Animal with provided id not found'
    }
    return Response(json.dumps(invalid_animal_msg), status=404, mimetype='application/json')


@app.route('/centers', methods=['GET'])
def get_centers():
    return jsonify({'centers': Center.get_all_centers()})


@app.route('/centers/<int:center_id>', methods=['GET'])
def get_center(center_id):
    return jsonify(Center.get_center(center_id))


@app.route('/register', methods=['POST'])
@error_handler
def add_center():
    request_data = request.get_json()
    center_id = Center.add_center(**request_data)
    response = Response('', status=201, mimetype='application/json')
    response.headers['Location'] = f'/centers/{center_id}'
    return response


@app.route('/species', methods=['GET'])
def get_all_species():
    species = [
        f'{inflect_engine.plural(species)} - {Species.get_animals_count_by_name(species)}'
        for species in Species.get_all_species()]
    return jsonify({'species': species})


@app.route('/species', methods=['POST'])
@jwt_required
@error_handler
def add_species():
    request_data = request.get_json()
    species_id = Species.add_species(**request_data)
    request_center = get_jwt_identity()
    log_data = {'method_type': request.method, 'req_url': request.path,
                'center_id': request_center,
                'entity_type': 'species', 'entity_id': species_id}
    file_logger.info('Species added', extra=log_data)
    response = Response('', status=201, mimetype='application/json')
    response.headers['Location'] = f'/species/{species_id}'
    return response


@app.route('/species/<int:species_id>', methods=['GET'])
def get_species(species_id):
    return jsonify(Species.get_species(species_id=species_id))
