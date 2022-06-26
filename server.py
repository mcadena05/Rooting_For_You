from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

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
    zipcode = request.form.get("zipcode")

    user = crud.get_user_by_email(email)
 
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(fname, lname, email, password, zipcode)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/plants")
def all_plants():
    # "View all plants."

    plants = crud.get_plants()

    return render_template("plant_selection.html", plants=plants)


@app.route("/plant/<plant_id>")
def show_plants(plant_id):
    # "Show growing and plant info"

    plant = crud.get_plant_by_id(plant_id)

    return render_template("plant_info.html", plant=plant)


@app.route("/login", methods=["POST"])
def process_login():
    # "Process user login."

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.fname}!")

    return render_template("user_details.html", user=user)


@app.route("/plant_selection", methods=["POST"])
def create_user_selected_plant_server():
    # "User selects plant"

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    user_selected_plant_list = request.form.getlist("plant_selection")
    plant_id= request.form.get('plant_id')
    plant = crud.get_plant_by_id(plant_id)

    if logged_in_email is None:
        flash("You must log in to select a plant for your garden.")
    elif user_selected_plant_list is None:
        flash("Error: you didn't select a plant.")
    else:
        for user_selected_plant in user_selected_plant_list:
            user_selected_plant = crud.create_user_selected_plant(user, plant)
            db.session.add(user_selected_plant)
            db.session.commit()

    # flash(f"You selected {user_selected_plant} for your garden!")

    
    return render_template("user_details.html", user=user, plant=plant)
 
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
