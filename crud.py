from model import db, User, Plant, UserSelectedPlant, connect_to_db
from datetime import datetime, date


def create_user(fname, lname, email, password, zipCodeTB):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password, zipCodeTB=zipCodeTB)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_plant(plant_id, name, description, spacing, watering, feeding, diseases, 
image_url, pests, harvesting, storage_use, optimal_sun,optimal_soil, transplanting, 
growing_from_seed, planting_considerations, when_to_plant, other_care  ):
   

    plant = Plant(
      
       plant_id= plant_id,
       name = name, 
       description= description, 
       spacing= spacing, 
       watering =watering, 
       feeding=feeding, 
       diseases=diseases, 
       image_url= image_url, 
       pests=pests, 
       harvesting=harvesting, 
       storage_use=storage_use, 
       optimal_sun=optimal_sun,
       optimal_soil=optimal_soil, 
       transplanting=transplanting, 
       growing_from_seed=growing_from_seed, 
       planting_considerations=planting_considerations,
       when_to_plant=when_to_plant, 
       other_care=other_care
 
       )

    return plant

def get_plants():
    """Return all plants."""

    return Plant.query.all()


def get_plant_by_id(plant_id):
    """Return a plant by primary key and api id."""

    return Plant.query.get(plant_id)

def get_plant_by_name(plant_id):
    """Return a plant by primary key and api id."""
    query_plant = Plant.query.get(plant_id)
    return query_plant.name


def create_user_selected_plant(user_id, plant_id):
    "function to create a selected plant "
    selected_plants = UserSelectedPlant(user_id=user_id, plant_id=plant_id)
    
    return selected_plants


def calculate_planting_date_range (zone):
    "function to determine frost date based off zone"
    last_frost_date_range= {'1a': ('05-22','06-04'), '1b': ('05-22','06-04'), '2a': ('05-15','05-22'), '2b': ('05-15','05-22'),
        '3a': ('05-01','05-16'), '3b': ('05-01','05-16'),'4a': ('04-24','05-12'), '4b': ('04-24','05-12'), '5a': ('04-07','04-30'), '5b': ('04-07','04-30'),
        '6a': ('04-01','04-21'), '6b': ('04-01','04-21'),'7a': ('03-22','04-03'), '7b': ('03-22','04-03'),'8a': ('03-13','03-28'), '8b': ('03-13','03-28'),
        '9a': ('02-06','02-28'), '9b': ('02-06','02-28')}
   
    return last_frost_date_range[zone]

   

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
