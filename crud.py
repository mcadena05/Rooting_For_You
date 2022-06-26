from model import db, User, Plant, UserSelectedPlant, connect_to_db
from datetime import datetime


def create_user(fname, lname, email, password, zipcode):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password, zipcode=zipcode)

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


def create_user_selected_plant(user_id, plant_id):
    "function to create a fake selected plant "
    selected_plants = UserSelectedPlant(user_id=user_id, plant_id=plant_id)

    return selected_plants

def calculate_planting_date_range ():
    "function to caluate optimal date range to plant a seed"
    return {
        "start_date": datetime.now(),
        "end_date": datetime.now() + datetime.timedelta(weeks=2),
    }

   

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
