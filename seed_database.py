"""Script to seed database."""

import os
import json
from random import choice

import crud
import model 
import server
import requests

os.system("dropdb my_garden")
os.system("createdb my_garden")

model.connect_to_db(server.app)
model.db.create_all()

# load zone data using zipcode
# def fetch_zone (zipCodeTB):
#     zone_api_clean =[]
#     response = requests.get(f'https://phzmapi.org/${zipCodeTB}.json')
#     zone= json.loads(response)
#     print(zone)

#     return zone

# api_key_variable =os.environ["HARVEST_HELPER_KEY"]
# print(api_key_variable)

# Load plant data from JSON file
api_clean = []

response = requests.get(f'http://harvesthelper.herokuapp.com/api/v1/plants?api_key=2798dab9fb946ade5389050cb1c43db3')
api_clean = json.loads(str(response.content, 'UTF-8'))

print(type(api_clean))



# Create plants, store them in list so we can use them
# to create fake user selected plants
plants_in_db = []
for plant in api_clean:
    
    plant_id, name, description, spacing, watering, feeding, diseases, image_url, pests, harvesting, storage_use, optimal_sun,optimal_soil, transplanting, growing_from_seed, planting_considerations, when_to_plant, other_care= (
    
        plant['id'],
        plant['name'],
        plant['description'],
        plant['spacing'],
        plant['watering'],
        plant['feeding'],
        plant['diseases'], 
        plant['image_url'],
        plant['pests'],
        plant['harvesting'],
        plant['storage_use'],
        plant['optimal_sun'],
        plant['optimal_soil'],
        plant['transplanting'],
        plant['growing_from_seed'],
        plant['planting_considerations'],
        plant['when_to_plant'],
        plant['other_care']
    )
    
    

  
    db_plant = crud.create_plant(
        
       plant_id,
       name, 
       description, 
       spacing, 
       watering, 
       feeding, 
       diseases, 
       image_url, 
       pests, 
       harvesting, 
       storage_use, 
       optimal_sun,
       optimal_soil, 
       transplanting, 
       growing_from_seed, 
       planting_considerations,
       when_to_plant, 
       other_care
       )

    plants_in_db.append(db_plant)

model.db.session.add_all(plants_in_db)
model.db.session.commit()

fake_zipcodes =['79936','10001', '93501','32244', '68003']
fake_fname= ['Jane', 'John']
fake_lname= ['Doe']

for n in range(10):
    email = f"user{n}@test.com" 
    password = "test"
    random_zipcode = choice(fake_zipcodes) 
    random_fname = choice(fake_fname) 

    user = crud.create_user(random_fname, fake_lname, email, password, random_zipcode)
    model.db.session.add(user)

    for _ in range(10):
        random_plant = choice(plants_in_db)
        
        user_random_plant = crud.create_user_selected_plant(user.user_id, random_plant.plant_id)
        model.db.session.add(user_random_plant)

companion_plant_dict = {"Asparagus": ['Calendula', 'Petunias', 'Tomatoes'], 
"Basil": ['Peppers', 'Purslane', 'Tomatoes'], "Beans": ['Beets', 'Corn', 'Lovage', 'Nasturtium', 'Rosemary', 'Squash', 'Strawberries', 'Sunflower'],
"Beets": ['Brassicas', 'Bush beans', 'Garlic', 'Lettuce', 'Onion family'], "Broccoli": ['Oregano', 'Cabbage', 'Brussels sprouts', 'Cauliflower'],
"Carrots": ['Chives', 'Leeks', 'Onions', 'Peas', 'Radishes', 'Rosemary', 'Sage'], "Corn": ['Beans', 'Cucumbers', 'Dill', 'Melons', 'Peas', 'Squash', 'Sunflower'],
"Cucumber": ['Beans', 'Borage', 'Dill', 'Lettuce', 'Nasturtiums', 'Oregano', 'Radish', 'Sunflower', 'Tansy'],
"Lettuce": ['Chives', 'Onions', 'Oregano', 'Peas', 'Egg plants', 'Poached ', 'Radish', 'Scallions', 'Zinnia'],
"Onion": ['Beets', 'Cabbage', 'Carrot', 'Chard', 'Lettuce', 'Strawberry ', 'Tomatoes'], 
"Peas": ['Alyssum', 'Carrot', 'Chives', 'Corn', 'Grapes', 'Lettuce ', 'Mint', 'Radish', 'Spinach', 'Turnip']  }  

plant_image_dic={
'Parsnips': 'static/images/Parsnips.png', 'Cabbage': 'static/images/Cabbage.png', 'Eggplant': 'static/images/Eggplant.png', 'Broccoli': 'static/images/Broccoli.png',
'Cantaloupe': 'static/images/Cantaloupe.png', 'Onion': 'static/images/Onion.png', 'Peas':'static/images/Peas.png', 'Turnips': 'https://unsplash.com/photos/EjICVrzSobA', 
'Thyme': 'static/images/Thyme.png', 'Collard Greens': 'static/images/CollardGreens.png',
}   
model.db.session.commit()