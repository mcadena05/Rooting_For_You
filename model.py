# model.py
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class User(db.Model):
    """Data model for a user information."""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    hashed = db.Column(db.String(100), nullable=False)
    zipCodeTB = db.Column(db.String, nullable=False)
    zone = db.Column(db.String, nullable=False)
    last_frost_date = db.Column(db.String, nullable=False)
    selected_plants = db.relationship('UserSelectedPlant',  backref="user")
    # garden = db.relationship('SqftGarden',  backref="user")
 
    
    
class Plant(db.Model):
    """Data model for an plants."""
    __tablename__ = "plants"

    plant_id  = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(50), nullable=False)
    description =db.Column(db.String)
    spacing = db.Column(db.Text)
    watering = db.Column(db.Text)
    feeding = db.Column(db.Text)
    diseases = db.Column(db.Text)
    image_url =db.Column(db.String)
    pests = db.Column(db.Text)
    harvesting = db.Column(db.Text)
    storage_use = db.Column(db.Text)
    optimal_sun = db.Column(db.Text)
    optimal_soil = db.Column(db.Text)
    transplanting = db.Column(db.Text)
    growing_from_seed = db.Column(db.Text)
    planting_considerations = db.Column(db.Text) 
    when_to_plant = db.Column(db.Text)
    other_care = db.Column(db.Text)
    companion_plants = db.Column(db.Text)
    image_png = db.Column(db.String)

    selected_plants = db.relationship('UserSelectedPlant',  backref="plant")
   


class UserSelectedPlant(db.Model):
    """Data model for the plants that were selected by the user"""

    __tablename__ = "user_selected_plants"
    
    user_plant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plant_id =  db.Column(db.Integer, db.ForeignKey("plants.plant_id"))
    user_id =  db.Column(db.Integer, db.ForeignKey("users.user_id")) 
    start_date = db.Column(db.Date)

    # plant = db.relationship("Plant", backref="user_selected_plants")   
    # user= db.relationship("User", backref="user_selected_plants")

# class SqftGarden(db.Model):
#     """Data model for a user information."""
#     __tablename__ = "sqft_garden"

#     garden_sqft  = db.Column(db.Integer, primary_key=True,autoincrement=True)  
#     user_id =  db.Column(db.Integer, db.ForeignKey("users.user_id")) 
#     grid_width = db.Column(db.Integer)
#     grid_length = db.Column(db.Integer)
#     grid_fill = db.Column(db.Text) 

    # def __str__(self):
    #     return f'{self.rows} x {self.cols}, fill {self.fill}'

    # def all_points(self):
    #     return [[row, col] for row in range(self.rows) for col in range(self.cols)]

    # def set_fill(self, value):
    #     self.fill_rows = json.dumps(value)

    # def get_fill(self):
    #     if self.fill == 'all':
    #         return self.all_points()
    #     else:
    #         return json.loads(self.fill)

    


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