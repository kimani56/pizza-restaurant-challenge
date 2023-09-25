from flask import Flask
from flask_migrate import Migrate

from models import db, Restaurant, RestaurantPizza


app = Flask(__name__)
app.config['SQL-ALCHEMY-URI'] =     'sqlite:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


if __name__ == '__main__':
    app.run(port=5555, debug=True)