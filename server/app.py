# #!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


class Home(Resource):
    def get(self):

        response = {
            "message": "Welcome to the Code Challenge API"
        } 
        return make_response(
            response,
            200
        )
api.add_resource(Home, "/")

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        my_restaurant_list = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
            for restaurant in restaurants
        ]
        response = make_response(
            jsonify(my_restaurant_list),
            200
        )
        return response

api.add_resource(Restaurants, "/restaurants")

class RestaurantById(Resource):
    def get(self, id):
        restaurants = Restaurant.query.filter_by(id=id).first()
        
        if restaurants:
            response = make_response(
                restaurants.to_dict(),
                200
            )
            return response
        else:
            return make_response(
                jsonify({"error": "Restaurant not found"}),
                404
            )

    def delete(self, id):
        restaurants = Restaurant.query.filter_by(id=id).first()

        if not restaurants:
            response = {
                "error": "Restaurant not found"
            }
            return make_response(
                jsonify(response),
                404
            )

        db.session.delete(restaurants)
        db.session.commit()
        response_dict = {
            "message": "Restaurant successfully deleted"
        }
        response = make_response(
            response_dict,
            204
        )
        return response

api.add_resource(RestaurantById, "/restaurants/<int:id>")

class Pizzas(Resource):
    def get(self):
        my_pizzas = Pizza.query.all()  
        my_pizza_list = [
            {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }
            for pizza in my_pizzas
        ]
        response = make_response(
            jsonify(my_pizza_list),
            200
        )
        return response

api.add_resource(Pizzas, "/pizzas")

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        
        try:
            new_pizza = RestaurantPizza(price=data["price"], pizza_id=data["pizza_id"], restaurant_id=data["restaurant_id"])
            db.session.add(new_pizza)
            db.session.commit()
        except ValueError:
            # Handling validation errors
            error_message = {
                "errors": ["validation errors"]
            }
            response = jsonify(error_message)
            return make_response(
                response,
                400
            )

        response_dict = new_pizza.to_dict()

        response = make_response(
            response_dict,
             201
            )
        return response

        
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")

if __name__ == '__main__':
    app.run(port=5555, debug=True)