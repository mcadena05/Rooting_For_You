from model import db, User, Plant, UserSelectedPlant, connect_to_db
from datetime import datetime, date
import requests
import json


def create_user(fname, lname, email, password, zipCodeTB):
    """Create and return a new user."""
    response = requests.get('https://phzmapi.org/'+ zipCodeTB +'.json')
    print(response.json())
    zone_api_response = response.json()

    zone= zone_api_response["zone"]

    last_frost_date_range= {'1a': 'May 22nd to Jun 4th', '1b': 'May 22nd to Jun 4th', '2a': 'May 15th to May 22nd', '2b': 'May 15th to May 22nd',
        '3a': 'May 1st to May 16th', '3b': 'May 1st to May 16th','4a': 'April 24th to May 12th', '4b': 'April 24th to May 12th', '5a': 'April 7th to April 30th', '5b': 'April 7th to April 30th',
        '6a': 'April 1st to April 21st', '6b': 'April 1st to April 21st','7a': 'March 22nd to April 3rd', '7b': 'March 22nd to April 3rd','8a': 'March 13th to April 28th', '8b': 'March 13th to April 28th',
        '9a': 'February 6th to February 28th', '9b': 'February 6th to February 28th'}

    last_frost_date = last_frost_date_range[zone]

    user = User(fname=fname, lname=lname, email=email, password=password, zipCodeTB=zipCodeTB, zone=zone, last_frost_date=last_frost_date)

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
growing_from_seed, planting_considerations, when_to_plant, other_care ):
   
    companion_plant_dict = {"Asparagus": 'Calendula, Petunias, Tomatoes', 
    "Basil": 'Peppers, Purslane, Tomatoes', "Beans": 'Beets, Corn, Lovage, Nasturtium, Rosemary, Squash, Strawberries, Sunflower',
    "Beets": 'Brassicas, Bush beans, Garlic, Lettuce, Onion family', "Broccoli": 'Oregano, Cabbage, Brussels sprouts, Cauliflower',
    "Carrots": 'Chives, Leeks, Onions, Peas, Radishes, Rosemary, Sage', "Corn": 'Beans, Cucumbers, Dill, Melons, Peas, Squash, Sunflower',
    "Cucumber": 'Beans, Borage, Dill, Lettuce, Nasturtiums, Oregano, Radish, Sunflower, Tansy',
    "Lettuce": 'Chives, Onions, Oregano, Peas, Egg plants, Poached, Radish, Scallions, Zinnia',
    "Onion": 'Beets, Cabbage, Carrot, Chard, Lettuce, Strawberry, Tomatoes', 
    "Peas": 'Alyssum, Carrot, Chives, Corn, Grapes, Lettuce, Mint, Radish, Spinach, Turnip',
    "Peppers": 'Basil, Marjoram, Onions, Oregano',
    "Potatoes": 'Basil, Beans, Calendula, Catmint, Cilantro, Garlic, Horseradish, Oregano, Peas, Tansy',
    "Winter Squash": 'Beans, Buckwheat, Calendula, Corn, Marigold, Nasturtium, Oregano',
    "Pumpkin": 'Beans, Buckwheat, Calendula, Corn, Marigold, Nasturtium, Oregano',
    "Radishes": 'Chervil, Lettuce, Nasturtium, Peas', 
    "Spinach": 'Beans, Cilantro, Eggplant, Oregano, Peas, Rosemary, Strawberries',
    "Tomatoes": 'Asparagus, Basil, Borage, Calendula, Dill, Garlic, Nasturtium, Onion, Parsley, Thyme',
    "Zucchini": 'Buckwheat, Oregano, Nasturtium, Zinnia',"Summer Squash": 'Buckwheat, Oregano, Nasturtium, Zinnia',
    "Parsnips": 'Peas, Beans, Peppers, Tomatoes, Lettuce, Rosemary, Sage',
    "Cabbage": 'Chamomile, Chives, Dill, Mint,Sage, Coriander, Geranium, Oregano, Thyme', 
    "Eggplant": 'Chamomile, Catnip, Dill, Oregano, Rosemary, Lavendar, Sage, Mint, Marigold, Sunflower', 
    "Cantaloupe":'Marigold, Nasturtiums, Radish, Lettuce',
    "Turnips": 'Brassicas, garlic, Peas, Beans Nasturtiums, Mint, Catnip, Thyme, Potatoes, Onions',
    "Thyme":'Strawberries, Cabbage, Tomatoes, Eggplant, Potatoes, Blueberries, Shallot, Roses',
    "Collard Greens": 'Catnip, Dill, Marigolds, Mint, Mustard Greens, Rosemary, Thyme',
    "Oregano": 'Peppers, Eggplant, Squash, Beans, Cabbage, Broccoli, Brussels Sprouts, Cauliflower, Turnips, Strawberries',
    "Parsley": 'Tomatoes, Chives, Carrots, Corn, Peppers, Onions, Pea',
    "Sage": 'Brocolli, Cauliflower, Rosemary, Cabbage, Carrots',
    "Dill":'Asparagus, Corn, Cucumbers, Onion, Lettuce, Brussels Sprouts, Broccoli, Basil',
    "Cilantro": 'Basil, Mint, Tansy, Tomatoes, Jalapeno, Peppers, Onion',
    "Kale": 'Artichokes, Beets, Celery, Cucumber, Lettuce, Onion, Peas, Potatoes',
    "Celery": 'Beans, Leeks, Onions, Cabbage, Spinach, Tomatoes',
    "Rhubarb": 'Broccoli, Cabbage, Kale, Cauliflower', 
    "Tarragon": 'Rosemary, Oregano, Sage, Lavender, Dill',
    "Sweet Corn": 'Basil, Dill, Nasturtiums, Beans, Potatoes, Pumpkins, Radish, Sunflowers',
    "Garlic": 'Cabbage, Chamomile, Peppers, Roses, Spinach, Strawberries',
    "Pumpkins": 'Oregano, Chives, Chamomile, Tansy, Radish, Nasturtium, Corn, Beans',
    "Chard": 'Cabbage, Celery, Thyme, Basil, Mint, Cilantro, Beans, Lettuce', 
    "Cauliflower": 'Beets, Broccoli, Brussels Sprouts, Chard, Spinach, Cucumber, Corn, Radish',
    "Mint": 'Oregano, Marigolds, Carrots, Cabbage, Cauliflower, Kale, Tomatoe, Eggplant, Peas, Beans',
    "Sweet Potato": 'Beets, Carrots, Parsnips',
    "Cucumbers": 'Peas, Corn, Beans, Lentils, Radish, Beets, Carrots, Onion',
    "Rosemary": 'Thyme, Sage, Onion, Shallot, Oregano, Lavender',
    "Chives": 'Grapes, Tomatoes, Carrots, broccoli, Cabbage, Eggplant, Peppers, Potatoes, Rhubarb, Roses, Squash, Strawberries',
    "Bell Peppers": 'Carrots, Cucumbers, Radishes, Squash, Spinach, Lettuce, Chard',
    "Brussels Sprouts": 'Beets, Beans, Carrots, Celery, Lettuce, Onion, Pea, Potatoe',
    "Watermelon": 'Sunflowers, Cosmos, Mint, Oregano, Thyme, Rosemary, Corn',
    "Okra": 'Calendula, Sunflowers, Nasturtiums, Radish, Cucumbers, Peppers, Melons, Lettuce, Basil'}  

    companion_plants = companion_plant_dict[name]

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
       other_care=other_care,
       companion_plants=companion_plants
 
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

 
# def calculate_planting_date_range (zone):
#     "function to determine frost date based off zone"
#     last_frost_date_range= {'1a': ('05-22','06-04'), '1b': ('05-22','06-04'), '2a': ('05-15','05-22'), '2b': ('05-15','05-22'),
#         '3a': ('05-01','05-16'), '3b': ('05-01','05-16'),'4a': ('04-24','05-12'), '4b': ('04-24','05-12'), '5a': ('04-07','04-30'), '5b': ('04-07','04-30'),
#         '6a': ('04-01','04-21'), '6b': ('04-01','04-21'),'7a': ('03-22','04-03'), '7b': ('03-22','04-03'),'8a': ('03-13','03-28'), '8b': ('03-13','03-28'),
#         '9a': ('02-06','02-28'), '9b': ('02-06','02-28')}

#     last_frost_date = last_frost_date_range[zone]
   
#     return last_frost_date

   

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
