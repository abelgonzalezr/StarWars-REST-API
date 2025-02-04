"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Planet_favorite, Character_favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.filter().all()
    result = list(map(lambda user: user.serialize(), users))

    response_body = {
        "user": result
    }

    return jsonify(response_body), 200


@app.route('/character', methods=['GET'])
def get_ch():
    users = User.query.filter().all()
    result = list(map(lambda user: user.serialize(), users))

    response_body = {
        "user": result
    }

    return jsonify(response_body), 200


@app.route('/character/<int:id>', methods=['GET'])
def get_characters(id):
    character = Character.query.get(id)
    print(character.serialize())
    result = {
        "personaje": character.serialize()
    }

    return jsonify(result), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    print(planet.serialize())
    result = {
        "planeta": planet_id
    }

    return jsonify(result), 200


@app.route('/planet', methods=['GET'])
def get_plane(planet_id):
    planet = Planet.query.get(planet_id)
    print(planet.serialize())
    result = {
        "planeta": planet_id
    }

    return jsonify(result), 200

@app.route('/planet_favorite/<int:user_id>', methods=['GET'])
def favorite_planet( user_id):
    favorite_planet= Planet_favorite.query.filter_by(user_id=user_id)
    result = list(map(lambda favorite: favorite.serialize(), favorite_planet))
    print(result[0])
    # resulti = {
    #     "favorite_planet": result[0].
    # }
    #  jsonify(resulti)
    return result[0], 200


@app.route('/planet_favorite', methods=['GET'])
def favorite_planets():


    return "planet_favorite", 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
