from functools import wraps

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import conjur

app = Flask(__name__)

conjur.config.url = 'http://possum'
conjur.config.account = 'example'

api = conjur.new_from_password('admin', 'secret')
key = api.role('host', 'petstore').rotate_api_key()
api = conjur.new_from_key('host/petstore', key)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://petstore:{}@appdb/petstore'.format(
    api.resource('variable', 'dbpassword').secret()
)
db = SQLAlchemy(app)


class Pets(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80), index=True)

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return '<Pet {}, {}>'.format(self.name, self.type)

db.create_all()


# This decorater validates that the user/host calling the route has privilege to do so
# Arguments
#   - resource: Kind and ID of a Possum resource, separated by : - example 'variable:dbpassword'
#   - privilege: The privilege the callers needs on the resource to be allowed to call the route
def validate_privilege(resource, privilege):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_token = request.headers.get('AUTHORIZATION')
            if auth_token is None:
                return jsonify({'ok': False, 'msg': 'Authorization header missing'}), 401

            _api = conjur.new_from_header(auth_token)
            kind, identifier = resource.split(':')
            if not _api.resource(kind=kind, identifier=identifier).permitted(privilege):
                return jsonify({'ok': False, 'msg': 'Not authorized'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/')
def home():
    return render_template('home.html', pets=Pets.query.all())


# API routes

@app.route('/api/pets', methods=['POST'])
@validate_privilege('host:petstore', 'add_pet')
def add_pet():
    json = request.get_json(force=True)
    valid = json.has_key('name') and json.has_key('type')

    if not valid:
        return jsonify({'ok': False, 'id': None, 'msg': "'name' or 'type' missing from JSON body"}), 400

    pet = Pets(json['name'], json['type'])
    db.session.add(pet)
    db.session.commit()

    return jsonify({'ok': True, 'id': pet.id}), 201


@app.route('/api/pets/<id>', methods=['DELETE'])
@validate_privilege('host:petstore', 'remove_pet')
def remove_pet(id):
    pet = Pets.query.filter_by(id=id).first()

    if pet is None:
        return jsonify({'ok': False, 'id': id, 'msg': 'Pet ID {} not found'.format(id)}), 404

    db.session.delete(pet)
    db.session.commit()

    return jsonify({'ok': True, 'id': id})

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)
