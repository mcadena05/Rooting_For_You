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


# Load plant data from JSON file
api_clean = []
def fetch_api():
    response = requests.get("http://harvesthelper.herokuapp.com/api/v1/plants?api_key=" + plant.name)
    print(response)
    api_clean.append(response)


# Create plants, store them in list so we can use them
# to create fake user selected plants
plants_in_db = []
for plant in api_clean:
    name, plant_species, plant_spacing ,  plant_watering, plant_fertilize, plant_diseases, plant_image_url,plant_pests,plant_harvesting,plant_use,plant_optimal_sun, plant_optimal_ph, plant_optimal_soil,plant_description,plant_transplant,plant_seed, planting_time,plant_recipes = (
        plant['name'],
        plant['plant_consideration'],
        plant['plant_spacing '],
        plant[' plant_watering'],
        plant['plant_fertilize'],
        plant['plant_diseases'],
        plant['plant_image'],
        plant['plant_pests'],
        plant['plant_harvesting'],
        plant['plant_use'],
        plant['plant_optimal_sun'],
        plant['plant_optimal_ph'],
        plant['plant_optimal_soil'],
        plant['plant_description'],
        plant['plant_transplant'],
        plant['plant_seed'],
        plant['planting_time'],
        plant['plant_recipes'],
    )
    
    db_plant = crud.create_plant(name,
       plant_species,
       plant_spacing ,
       plant_watering,
       plant_fertilize,
       plant_diseases ,
       plant_image_url,
       plant_pests,
       plant_harvesting,
       plant_use,
       plant_optimal_sun,
       plant_optimal_ph,
       plant_optimal_soil,
       plant_description,
       plant_transplant,
       plant_seed,
       planting_time,
       plant_recipes
       )

    plants_in_db.append(db_plant)

model.db.session.add_all(plants_in_db)
model.db.session.commit()

for n in range(10):
    email = f"user{n}@test.com" 
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_plant = choice(plants_in_db)
        
        user_random_plant = crud.create_user_selected_plant(user, random_plant)
        model.db.session.add(user_random_plant)

model.db.session.commit()