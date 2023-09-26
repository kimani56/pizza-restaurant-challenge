from random import randint, choice as rc

from faker import Faker

from app import app 
from models import db, Restaurant, RestaurantPizza, Pizza

fake = Faker()

with app.app_context():
    Restaurant.query.delete()
    RestaurantPizza.query.delete()
    Pizza.query.delete()

    pizzas = []
    toppings = [
        "Pepperoni",
        "Mushrooms",
        "Onions",
        "Sausage",
        "Bacon",
        "Extra Cheese",
        "Green Peppers",
        "Black Olives",
        "Pineapple",
        "Spinach",
        "Jalapenos",
        "Artichoke Hearts",
        "Anchovies",
        "Tomatoes",
        "Ham",
        "Chicken",
        "Feta Cheese",
    ]

    def generate_name():
        num = fake.random_int(min=1, max=len(toppings))
        selected = [toppings[i] for i in range(num) ]
        return f"{', '.join(selected)} Pizza"
    
    for i in range(10):
        pizza_name = generate_name()
        final = Pizza(name=pizza_name, ingredients=rc(toppings))
        pizzas.append(final)

    db.session.add(pizzas)

    restaurants = []
    for i in range(10):
        fakes = Restaurant(name=fake.company(), adress=fake.adress())
        restaurants.append(fakes)
         
        db.session.add_all(restaurants)


    restaurant_pizzas = []
    for i in range(20):
        rp = RestaurantPizza(price=randint(1, 30), pizza_id=randint(1, 10), restaurant_id=randint(1, 10))