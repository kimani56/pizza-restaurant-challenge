from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from server.exceptions import ValueInputException
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})


db = SQLAlchemy(metadata=metadata)

class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurants = db.relationship(
        "Restaurant", secondary="restaurant_pizzas", back_populates="pizzas"
    )

    @classmethod
    def get_pizza_by_id(cls, id):
        return cls.query.get(id)

    def __repr__(self):
        return f"<Pizza {self.name}>"

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String)

    pizzas = db.relationship(
        "Pizza", secondary="restaurant_pizzas", back_populates="restaurants"
    )

    @validates("name")
    def validate_name(self, key, name):
        if len(name.strip().split()) >= 50:
            raise ValueInputException("Must have a name less than 50 words in length")

        existing_restaurant = Restaurant.query.filter_by(name=name).first()
        if existing_restaurant:
            raise ValueInputException("Name value must be unique")

        return name

    def __repr__(self):
        return f"<Restaurant {self.name} {self.address}>"

class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(
        db.Integer,
        db.CheckConstraint(
            "price >= 1 AND price <= 30",
            name="price_within_range"
        ),
    )
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("price")
    def validate_price(self, key, price):
        if not isinstance(price, int) or not (1 <= price <= 30):
            raise ValueInputException("Must have a price between 1 and 30")

        return price

    @classmethod
    def create_restaurant_pizza(cls, price, pizza_id, restaurant_id):
        rp = cls(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(rp)
        db.session.commit()
        return Pizza.get_pizza_by_id(pizza_id)

    def __repr__(self):
        return f"<RestaurantPizza {self.price}>"
