import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Render main page
@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)


# Render registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists in database.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        flash("existing_user")

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
            
        register_details = {
            "username": request.form.get("username").lower(),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "company": request.form.get("company"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register_details)
        
        # Put user into session cookie.
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# Render login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            # Check hashed password against password provided.
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for("profile", username=session["user"]))
            else:
                # Display message in case password incorrect.
                flash("Incorrect username or password")
                return redirect(url_for("login"))
        else:
            # Display message in case username incorrect.
            flash("Incorrect username or password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Render user profile page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one({"username": session["user"]})["username"]
    first_name = mongo.db.users.find_one({"username": session["user"]})["first_name"]
    last_name = mongo.db.users.find_one({"username": session["user"]})["last_name"]
    company = mongo.db.users.find_one({"username": session["user"]})["company"]

    if session["user"]:
        return render_template("profile.html", username=username,
            first_name=first_name, last_name=last_name, company=company)

    return redirect(url_for("login"))


# Logout function
@app.route("/logout")
def logout():
    # remove session from cookies
    flash("You've been safely logged out.")
    session.pop("user")
    return redirect(url_for("login"))


# Manage section
# Render electrical rooms page
@app.route("/get_rooms")
def get_rooms():
    rooms = list(mongo.db.electricalRooms.find())
    return render_template("rooms.html", rooms=rooms)

# Main function
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
