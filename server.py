from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db,  User, Plant, UserSelectedPlant, db
import crud
from passlib.hash import argon2

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    # "View homepage."

    return render_template("homepage.html")


@app.route("/users")
def all_users():
    # "View all users."

    users = crud.get_users()

    return render_template("all_users.html", users=users)
    

@app.route("/users/<user_id>")
def show_user(user_id):
    # """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/users", methods=["POST"])
def register_user():
    # "Create a new user."

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    zipCodeTB = request.form.get("zipCodeTB")

    hashed = argon2.hash(password)

    del password

    user = crud.get_user_by_email(email)
 
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(fname, lname, email, hashed, zipCodeTB)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/plants")
def all_plants():
    # "View all plants."

    plants = crud.get_plants()

    return render_template("plant_selection.html", plants=plants)


@app.route("/plants/<plant_id>")
def show_plant(plant_id):
    # """Show details on a plant in garden."""

    plant = crud.get_plant_by_id(plant_id)

    return render_template("plant_info.html", plant=plant)


@app.route("/login", methods=["POST"])
def process_login():
    # "Process user login."

    email = request.form.get("email")
    password_attempt = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or not argon2.verify(password_attempt , user.hashed):
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    elif argon2.verify(password_attempt , user.hashed):
        session["user_email"] = user.email
        flash(f"Welcome back, {user.fname}!")
        return redirect(f"/users/{user.user_id}")

@app.route("/plant_selection", methods=["POST"])
def create_user_selected_plant_server():
    
    logged_in_email = session.get("user_email")
    selected_plants_list = request.form.getlist("plant_options")
    user = crud.get_user_by_email(logged_in_email)
    
    if logged_in_email is None:
        flash("You must log to select a plant for your garden.")
    elif not selected_plants_list:
        flash("Error: you didn't select a plant for your garden!")
    else:
        selected_plant_list_by_name = []
        for selected_plant in selected_plants_list:
            user_selected_plant = crud.create_user_selected_plant(user.user_id, selected_plant)
            name_selected_plant = crud.get_plant_by_name(selected_plant)
            selected_plant_list_by_name.append(name_selected_plant)
            db.session.add(user_selected_plant)
            db.session.commit()
        
      
        flash(f"You have selected {selected_plant_list_by_name} to grow in your garden.")

    return render_template("user_details.html", user=user)
 
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
