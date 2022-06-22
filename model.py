# model.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Data model for a user information."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

    plants = db.relationship("Plant", secondary="user_selected_plants", backref="users")    
    
class Plant(db.Model):
    """Data model for an plants."""
    __tablename__ = "plants"


    plant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    plant_consideration = db.Column(db.String)
    plant_spacing = db.Column(db.Text)
    plant_watering = db.Column(db.Text)
    plant_fertilizer = db.Column(db.Text)
    plant_diseases = db.Column(db.Text)
    plant_image_url = db.Column(db.String)
    plant_pests = db.Column(db.Text)
    plant_harvesting = db.Column(db.Text)
    plant_use = db.Column(db.Text)
    plant_optimal_sun = db.Column(db.Text)
    plant_optimal_ph = db.Column(db.Text)
    plant_optimal_soil = db.Column(db.Text)
    plant_description =db.Column(db.Text)
    plant_transplant = db.Column(db.Text)
    plant_seed = db.Column(db.Text)
    planting_time = db.Column(db.Text)
    plant_recipes= db.Column(db.Text)

    # backref allowed for access to users (magic attribute)


class UserSelectedPlant(db.Model):
    """Data model for the plants that were selected by the user"""

    __tablename__ = "user_selected_plants"

    user_plant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plant_id =  db.Column(db.Integer, db.ForeignKey("plants.plant_id"))
    user_id =  db.Column(db.Integer, db.ForeignKey("users.user_id")) 
    start_date = db.Column(db.Date)


def connect_to_db(flask_app, db_uri="postgresql:///my_garden", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()