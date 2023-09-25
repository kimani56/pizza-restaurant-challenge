from models import Restaurant, Pizza, RestaurantPizza, db
from exceptions import RestaurantNotFoundException, ValueInputException


class RestaurantService:
    @classmethod
    def get_all_restaurants(cls):
        restaurants = Restaurant.query.all()
        return restaurants

    @classmethod
    def get_restaurant_by_id(cls, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            return restaurant
        else:
            raise RestaurantNotFoundException("Restaurant not found")

    @classmethod
    def delete_restaurant_by_id(cls, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            rest_pizzs = RestaurantPizza.query.filter_by(restaurant_id=id).all()
            for rp in rest_pizzs:
                db.session.delete(rp)
            db.session.commit()
            db.session.delete(restaurant)
            db.session.commit()
            return {}
        else:
            raise RestaurantNotFoundException("Restaurant not found")


class PizzaService:
    @classmethod
    def get_all_pizzas(cls):
        pizzas = Pizza.query.all()
        return pizzas


class RestaurantPizzaService:
    @classmethod
    def get_all_restaurant_pizzas(cls):
        restaurant_pizzas = RestaurantPizza.query.all()
        return restaurant_pizzas

    @classmethod
    def create_restaurant_pizza(cls, **kwargs):
        try:
            pizza = RestaurantPizza.create_restaurant_pizza(**kwargs)
            return pizza
        except ValueInputException as e:
            raise e
