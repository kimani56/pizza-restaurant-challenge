from flask import make_response, request
from flask_restful import Resource
from marshmallow import Schema, fields
from app import rest_api

from services import RestaurantService, PizzaService, RestaurantPizzaService
from exceptions import RestaurantNotFoundException, ValueInputException


class RestaurantSchema(Schema):
    class Meta:
        fields = ("id", "name", "address")


restaurants_schema = RestaurantSchema(many=True)


class PizzaSchema(Schema):
    class Meta:
        fields = ("id", "name", "ingredients")


pizzas_schema = PizzaSchema(many=True)
pizza_schema = PizzaSchema()


class RestaurantByIdSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    address = fields.String()
    pizzas = fields.Nested(PizzaSchema, many=True)


restaurant_by_id_schema = RestaurantByIdSchema()


class RestaurantPizzaSchema(Schema):
    price = fields.Integer()
    pizza_id = fields.Integer()
    restaurant_id = fields.Integer()


restaurant_pizzas_schema = RestaurantPizzaSchema(many=True)


class HomeResource(Resource):
    def get(self):
        return {"message": "Flask Code Challenge - Pizza Restaurants"}


rest_api.add_resource(HomeResource, "/")


class PizzaResourse(Resource):
    def get(self):
        pizzas = PizzaService.get_all_pizzas()

        response = make_response(
            pizzas_schema.dumps(pizzas),
            200,
            {"Content-Type": "application/json"},
        )

        return response


rest_api.add_resource(PizzaResourse, "/pizzas")


class RestaurantResourse(Resource):
    def get(self):
        restaurants = RestaurantService.get_all_restaurants()

        response = make_response(
            restaurants_schema.dumps(restaurants),
            200,
            {"Content-Type": "application/json"},
        )

        return response


rest_api.add_resource(RestaurantResourse, "/restaurants")


class RestaurantByIdResourse(Resource):
    def get(self, id):
        try:
            restaurant = RestaurantService.get_restaurant_by_id(id)

            response = make_response(
                restaurant_by_id_schema.dumps(restaurant),
                200,
                {"Content-Type": "application/json"},
            )
            return response
        except RestaurantNotFoundException as e:
            return self.__restaurant_not_found_response(e)

    def delete(self, id):
        try:
            restaurant = RestaurantService.delete_restaurant_by_id(id)

            response = make_response(
                restaurant_by_id_schema.dumps(restaurant),
                204,
                {"Content-Type": "application/json"},
            )
            return response
        except RestaurantNotFoundException as e:
            return self.__restaurant_not_found_response(e)

    def __restaurant_not_found_response(self, e):
        message = {"error": str(e)}
        response = make_response(message, 404, {"Content-Type": "application/json"})
        return response


rest_api.add_resource(RestaurantByIdResourse, "/restaurants/<int:id>")


class RestaurantPizzaResourse(Resource):
    def get(self):
        restaurant_pizzas = RestaurantPizzaService.get_all_restaurant_pizzas()

        response = make_response(
            restaurant_pizzas_schema.dumps(restaurant_pizzas),
            200,
            {"Content-Type": "application/json"},
        )

        return response

    def post(self):
        try:
            data = request.get_json()
            pizza = RestaurantPizzaService.create_restaurant_pizza(**data)

            response = make_response(
                pizza_schema.dumps(pizza),
                200,
                {"Content-Type": "application/json"},
            )

            return response
        except ValueInputException as e:
            message = {"errors": e.args}
            response = make_response(message, 400, {"Content-Type": "application/json"})
            return response


rest_api.add_resource(RestaurantPizzaResourse, "/restaurant_pizzas")
