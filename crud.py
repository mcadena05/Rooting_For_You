from model import db, User, Plant, UserSelectedPlant, connect_to_db


def create_user(fname, lname, email, password, zipcode):
    

    user = User(fname=fname, lname=lname, email=email, password=password, zipcode=zipcode)

    return user


def create_plant(name, plant_species,plant_spacing,plant_watering,plant_fertilize,plant_diseases,plant_image_url,
plant_pests,plant_harvesting,plant_use,plant_optimal_sun,plant_optimal_ph,plant_optimal_soil,plant_description,
plant_transplant,plant_seed,planting_time,plant_recipes):
   

    plant = Plant(
       name=name,
       plant_species=plant_species,
       plant_spacing=plant_spacing,
       plant_watering=plant_watering,
       plant_fertilize=plant_fertilize,
       plant_diseases=plant_diseases,
       plant_image_url=plant_image_url,
       plant_pests=plant_pests,
       plant_harvesting=plant_harvesting,
       plant_use=plant_use,
       plant_optimal_sun=plant_optimal_sun,
       plant_optimal_ph=plant_optimal_ph, 
       plant_optimal_soil=plant_optimal_soil,
       plant_description=plant_description,
       plant_transplant=plant_transplant,
       plant_seed=plant_seed,
       planting_time=planting_time,
       plant_recipes=plant_recipes
 
       )

    return plant


def create_user_selected_plant(user, plant, start_date):
  

    selected_plants = UserSelectedPlant(user=user, plant=plant, start_date=start_date)

    return selected_plants


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
