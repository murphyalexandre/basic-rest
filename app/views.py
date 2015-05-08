from flask import abort, Blueprint, jsonify, request
from app import db
from .models import Car

basic_rest = Blueprint(
    'basic-rest',
    __name__,
    template_folder='templates'
)


@basic_rest.route('/api/v1/cars', methods=['GET'])
def car_list():
    """ API Endpoint to show car list """
    return jsonify(results=[c.serialize for c in Car.query.all()])


@basic_rest.route('/api/v1/cars/<int:id>', methods=['GET'])
def car(id):
    """ API Endpoint to show car by id """
    return jsonify(Car.query.get_or_404(id).serialize)


@basic_rest.route('/api/v1/cars', methods=['POST'])
def new_car():
    """ API Endpoint to add a new car """
    try:
        data = request.get_json(force=True)

        # Insert new car
        new_car = Car(
            description=data['description'],
            cylinders=data['cylinders'],
            make=data['make'],
            model=data['model'],
            year=data['year'],
            owner=data['owner'],
            image=data['image']
        )
        db.session.add(new_car)
        db.session.commit()

        return jsonify(new_car.serialize)
    except KeyError:
        abort(400)


@basic_rest.route('/api/v1/cars/<int:id>', methods=['PUT'])
def update_car(id):
    """ API Endpoint to update a car """
    try:
        data = request.get_json(force=True)

        # Find the car to update
        found = Car.query.get_or_404(id)

        # Partial updates with ternary operator
        found.description = data['description'] \
            if 'description' in data else found.description
        found.cylinders = data['cylinders'] \
            if 'cylinders' in data else found.cylinders
        found.make = data['make'] if 'make' in data else found.make
        found.model = data['model'] if 'model' in data else found.model
        found.year = data['year'] if 'year' in data else found.year
        found.owner = data['owner'] if 'owner' in data else found.owner
        found.image = data['image'] if 'image' in data else found.image

        db.session.commit()

        return jsonify(found.serialize)
    except KeyError:
        abort(400)


@basic_rest.route('/api/v1/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    """ API Endpoint to delete a car by id """
    db.session.delete(Car.query.get_or_404(id))
    db.session.commit()

    return ('', 204)
