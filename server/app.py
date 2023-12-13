#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        response_dict = {
            "index": "Welcome to the Plant Store API",
        }
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

api.add_resource(Index, '/')

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        response_dict_list = [plant.to_dict() for plant in plants]
        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            response_dict = plant.to_dict()
            response = make_response(
                jsonify(response_dict),
                200,
            )
        else:
            response_dict = {"error": "Plant not found"}
            response = make_response(
                jsonify(response_dict),
                404,
            )
        return response

api.add_resource(PlantByID, '/plants/<int:plant_id>')

class CreatePlant(Resource):
    def post(self):
        try:
            data = request.json  
            new_plant = Plant(
                name=data['name'],
                image=data['image'],
                price=float(data['price']), 
            )
            db.session.add(new_plant)
            db.session.commit()

            new_plant_id = new_plant.id

            response_dict = new_plant.to_dict()
            response_dict['id'] = new_plant_id  
            response = make_response(
                jsonify(response_dict),
                201,
            )
            return response
        except Exception as e:
            print(f"Exception during plant creation: {e}")
            response_dict = {"error": "Failed to create plant"}
            response = make_response(
                jsonify(response_dict),
                500, 
            )
            return response

api.add_resource(CreatePlant, '/plants/create')

if __name__ == '__main__':
    app.run(port=5555)
