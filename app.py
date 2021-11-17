# CODE ATTRIBUTION:
# The code for this website is based on the excellent Data Centric Design
# Mini Project Walk-through by Tim Nelson (https://github.com/TravelTimN)
# of Code Institute. Where custom functionality was required it was
# generally based on modifying Tim's original logic to fulfill the
# project requirements.

import os
import datetime
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


# CODE CREDIT https://newbedev.com/accessing-python-dict-values-with-the-key-start-characters # noqa


def value_by_key_prefix(dictionary, partial):
    """
    Function to search a dictionary with partial key
    and return the first match.
    """
    matches = [val for key,
               val in dictionary.items()
               if key.startswith(partial)]
    if not matches:
        raise KeyError(partial)
    if len(matches) > 1:
        raise ValueError('{} matches more than one key'.format(partial))
    return matches[0]


def key_prefixes(dictionary, partial):
    """
    Function to search a dictionary with partial key
    and return all matching keys.
    """
    matches = [key for key,
               val in dictionary.items()
               if key.startswith(partial)]
    if not matches:
        raise KeyError(partial)
    return matches

# END CODE CREDIT


@app.route("/")
def get_overview():
    """
    Render main page
    """
    rooms = list(mongo.db.electricalRooms.find())
    return render_template("overview.html", rooms=rooms)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Render the registration page.
    """
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


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Render the login page.
    """
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Check hashed password against password provided.
            if check_password_hash(
                existing_user["password"],
                    request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(
                    url_for("profile", username=session["user"]))
            else:
                # Display message in case password incorrect.
                flash("Incorrect username or password")
                return redirect(url_for("login"))
        else:
            # Display message in case username incorrect.
            flash("Incorrect username or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Logout function.
    Remove user session from cookies.
    """
    flash("You've been safely logged out.")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Render the user profile page.
    """
    user = mongo.db.users.find_one(
        {"username": session["user"]})

    if session["user"]:
        return render_template(
            "profile.html",
            user=user)

    return redirect(url_for("login"))


@app.route("/survey/new", methods=["GET", "POST"])
def new_survey():
    """
    Render the new survey page.
    """
    if request.method == "POST":
        # Retreive the room ref, comments, who and when data from the page.
        # Store these in a dictionary.
        new_report = {
            "roomRef": request.form.get("room_ref"),
            "surveyComment": request.form.get("survey_comment"),
            "createdBy": session["user"],
            "createdAt": datetime.datetime.now(),
        }
        # Get the list of questions from Mongo.
        questions = list(mongo.db.surveyQuestions.find().sort("_id", 1))
        # Loop through the list of questions to pull each answer.
        for question in questions:
            # Grab the question number, e.g. "1_01"
            question_no = question["questionNumber"]
            # Create the answer name, e.g. "answer_1_01"
            answer_id = "answer_" + str(question_no)
            # Retreive this answer name from the POST data.
            new_answer = request.form.get(answer_id)
            # Append this to the report dictionary.
            new_report[answer_id] = new_answer
            # Repeat loop through all questions.
        # Insert this dictionary into the DB as a new survey report
        mongo.db.surveyReports.insert_one(new_report)
        flash("New electrical report submitted.")
        return redirect(url_for("get_overview"))
    rooms = list(mongo.db.electricalRooms.find().sort("_id", 1))
    questions = list(mongo.db.surveyQuestions.find().sort("_id", 1))
    voltages = list(mongo.db.voltages.find().sort("_id", 1))
    types = list(mongo.db.roomTypes.find().sort("_id", 1))
    return render_template("new-survey.html", rooms=rooms, questions=questions,
                           voltages=voltages, types=types)


@app.route("/surveys")
def survey_list():
    """
    Render the survey list page.
    """
    # Query MongoDB for Survey Reports and turn it into a list.
    survey_reports = list(mongo.db.surveyReports.find().sort("_id", 1))
    # Create a new list for holding the fully rendered issues to be sent to html.
    rendered_survey_reports = []
    # Loop through Mongo DB's returned list.
    for parrot in survey_reports:
        room_ref = parrot['roomRef']
        # Look up electricalRooms collection to get room type, description and voltage.
        room_dictionary = mongo.db.electricalRooms.find_one(
                                {"roomRef": room_ref})
        room_type = room_dictionary['roomType']
        room_desc = room_dictionary['roomDesc']
        room_volts = room_dictionary['roomVolts']
        # Get the comment added by the surveyor.
        survey_comment = parrot['surveyComment']
        # Look up user collection to get the surveyor's full name and company.
        created_by = parrot['createdBy']
        created_by_dictionary = mongo.db.users.find_one(
                                {"username": created_by})
        created_by_fullname = (created_by_dictionary['first_name']
                               + " " + created_by_dictionary['last_name'])
        created_by_company = created_by_dictionary['company']
        # Convert date time stamp to full text formatting.
        created_at = parrot['createdAt'].strftime("%A, %d. %B %Y %I:%M%p")
        created_at_short = parrot['createdAt'].strftime("%d/%m/%y")
        answer_list = []
        count_pass = 0
        count_fail = 0
        count_nc = 0
        count_na = 0
        answer_keys = key_prefixes(parrot, "answer_")
        for key in answer_keys:
            answer_no = key
            answer_value = parrot[answer_no]
            if answer_value == "Pass":
                count_pass = count_pass + 1
            elif answer_value == "Fail":
                count_fail = count_fail + 1
            elif answer_value == "NC":
                count_nc = count_nc + 1
            elif answer_value == "NA":
                count_na = count_na + 1
            question_no = answer_no[-4:]
            question_dictionary = mongo.db.surveyQuestions.find_one(
                                    {"questionNumber": question_no})
            question_short = question_dictionary['questionShort']
            question_long = question_dictionary['questionLong']
            new_answer = {
                "questionNumber": question_no,
                "questionShort": question_short,
                "questionLong": question_long,
                "answerValue": answer_value,
            }
            answer_list.append(new_answer)
        # Pack all values into a dictionary and append it to the
        # rendered_survey_issues list.
        report = {
            'roomRef': room_ref,
            'roomType': room_type,
            'roomDesc': room_desc,
            'roomVolts': room_volts,
            'surveyComment': survey_comment,
            'createdBy': created_by,
            'createdByFullname': created_by_fullname,
            'createdByCompany': created_by_company,
            'createdAt': created_at,
            'createdAtShort': created_at_short,
            'answerList': answer_list,
            'countPass': count_pass,
            'countFail': count_fail,
            'countNC': count_nc,
            'countNA': count_na,
        }
        rendered_survey_reports.append(report)
    return render_template("survey-list.html",
                           rendered_survey_reports=rendered_survey_reports,)


@app.route("/issue/new", methods=["GET", "POST"])
def new_issue():
    """
    Render New Issue Page
    """
    if request.method == "POST":
        issue = {
            "roomRef": request.form.get("room_ref"),
            "questionNumber": request.form.get("question_no"),
            "issueComment": request.form.get("issue_comment"),
            "createdBy": session["user"],
            "createdAt": datetime.datetime.now(),
        }
        mongo.db.surveyIssues.insert_one(issue)
        flash("New electrical issue raised.")
        return redirect(url_for("get_overview"))
    rooms = list(mongo.db.electricalRooms.find().sort("_id", 1))
    questions = list(mongo.db.surveyQuestions.find().sort("_id", 1))
    voltages = list(mongo.db.voltages.find().sort("_id", 1))
    types = list(mongo.db.roomTypes.find().sort("_id", 1))
    return render_template("new-issue.html",
                           rooms=rooms,
                           questions=questions,
                           voltages=voltages,
                           types=types)


@app.route("/issues")
def issue_list():
    """
    Render issues list page.
    """
    # Query MongoDB for Survey Issues and turn it into a list.
    survey_issues = list(mongo.db.surveyIssues.find().sort("_id", -1))
    # Create a new list for holding the fully rendered issues to be sent to html.
    rendered_survey_issues = []
    # Loop through Mongo DB's returned list.
    for budgie in survey_issues:
        issue_id = budgie['_id']
        room_ref = budgie['roomRef']
        # Look up electricalRooms collection to get room type, description and voltage.
        room_dictionary = mongo.db.electricalRooms.find_one(
                            {"roomRef": room_ref})
        room_type = room_dictionary['roomType']
        room_desc = room_dictionary['roomDesc']
        room_volts = room_dictionary['roomVolts']
        # Look up surveyQuestions collection to get full question texts.
        question_no = budgie['questionNumber']
        question_dictionary = mongo.db.surveyQuestions.find_one(
                            {"questionNumber": question_no})
        question_short = question_dictionary['questionShort']
        question_long = question_dictionary['questionLong']
        # Get the comment added by the surveyor.
        issue_comment = budgie['issueComment']
        # Look up user collections to get the surveyor's full name and company
        created_by = budgie['createdBy']
        created_by_dictionary = mongo.db.users.find_one(
                                    {"username": created_by})
        created_by_fullname = (created_by_dictionary['first_name']
                               + " " + created_by_dictionary['last_name'])
        created_by_company = created_by_dictionary['company']
        # Convert date time stamp to full text formatting.
        created_at = budgie['createdAt'].strftime("%A, %d. %B %Y %I:%M%p")
        created_at_short = budgie['createdAt'].strftime("%d/%m/%y")
        # Pack all values into a dictionary and append it to the
        # rendered_survey_issues list.
        issue = {
            '_id': issue_id,
            'roomRef': room_ref,
            'roomType': room_type,
            'roomDesc': room_desc,
            'roomVolts': room_volts,
            'questionNumber': question_no,
            'questionShort': question_short,
            'questionLong': question_long,
            'issueComment': issue_comment,
            'createdBy': created_by,
            'createdByFullname': created_by_fullname,
            'createdByCompany': created_by_company,
            'createdAt': created_at,
            'createdAtShort': created_at_short,
        }
        rendered_survey_issues.append(issue)
    return render_template("issue-list.html",
                           rendered_survey_issues=rendered_survey_issues)


@app.route("/delete_issue/<issue_id>")
def delete_issue(issue_id):
    """
    Delete an electrical issue function
    """
    mongo.db.surveyIssues.remove({"_id": ObjectId(issue_id)})
    flash("Issue successfully deleted.")
    return redirect(url_for("issue_list"))


@app.route("/edit_issue/<issue_id>")
def edit_issue(issue_id):
    """
    Edit an electrical issue function
    """
    flash("testhigh.")  # testhigh
    return redirect(url_for("issue_list"))

# Manage section


@app.route("/get_room_list")
def get_room_list():
    """
    Render the electrical rooms list.
    """
    rooms = list(mongo.db.electricalRooms.find())
    return render_template("room-list.html", rooms=rooms)


@app.route("/edit_room/<room_id>", methods=["GET", "POST"])
def edit_room(room_id):
    """
    Render the page to edit an individual electrical room's details.
    """
    if request.method == "POST":
        edited_room = {
            "roomRef": request.form.get("room_ref"),
            "roomDesc": request.form.get("room_desc"),
            "roomVolts": request.form.get("room_volts"),
            "roomType": request.form.get("room_type"),
            "editedBy": session["user"]
        }
        mongo.db.electricalRooms.update(
            {"_id": ObjectId(room_id)}, edited_room)
        flash("Electrical room edited successfully.")
        return redirect(url_for("get_room_list"))
    room = mongo.db.electricalRooms.find_one({"_id": ObjectId(room_id)})
    voltages = list(mongo.db.voltages.find().sort("_id", 1))
    types = list(mongo.db.roomTypes.find().sort("_id", 1))
    return render_template(
        "edit_room.html",
        room=room,
        voltages=voltages,
        types=types)


@app.route("/delete_room/<room_id>")
def delete_room(room_id):
    """
    Delete an electrical room function
    """
    mongo.db.electricalRooms.remove({"_id": ObjectId(room_id)})
    flash("Room successfully deleted.")
    return redirect(url_for("get_rooms_list"))


@app.route("/add_room", methods=["GET", "POST"])
def add_room():
    """
    Add an electrical room function.
    """
    if request.method == "POST":
        new_room = {
            "roomRef": request.form.get("room_ref"),
            "roomDesc": request.form.get("room_desc"),
            "roomVolts": request.form.get("room_volts"),
            "roomType": request.form.get("room_type"),
            "createdBy": session["user"]
        }
        mongo.db.electricalRooms.insert_one(new_room)
        flash("New electrical room added successfully.")
        return redirect(url_for("get_overview"))
    voltages = list(mongo.db.voltages.find().sort("_id", 1))
    types = list(mongo.db.roomTypes.find().sort("_id", 1))
    return render_template("addroom.html", voltages=voltages, types=types)


@app.route("/survey_question_list")
def survey_question_list():
    """
    Render survey questions list page
    """
    questions = list(mongo.db.surveyQuestions.find().sort("_id", 1))
    return render_template("survey-question-list.html", questions=questions)


@app.route("/survey_question_edit", methods=["GET", "POST"])
def survey_question_edit(question_id):
    """
    Render survey questions edit page
    """
    if request.method == "POST":
        edited_question = {
            "questionShort": request.form.get("question_short"),
            "questionLong": request.form.get("question_long"),
            "editedBy": session["user"]
        }
        mongo.db.surveyQuestions.update(
            {"_id": ObjectId(question_id)}, edited_question)
        flash("Survey question edited successfully.")
        return redirect(url_for("survey_question_list"))

    questions = list(mongo.db.surveyQuestions.find().sort("_id", 1))
    return render_template("survey-question-edit.html", questions=questions)


# Render test page testhigh to be deleted
@app.route("/test_page")
def test_page():
    # reports = list(mongo.db.surveyReport.find_one())
    # questions = list(mongo.db.surveyQuestions.find().sort("_id", 1))
    now = datetime.datetime.now()
    date_time_string = now.strftime("%A, %d. %B %Y %I:%M%p")
    # testing code here for renedering survey issues testhigh------------------------------------------------
    
    # Query MongoDB for Survey Issues and turn it into a list.
    survey_issues = list(mongo.db.surveyIssues.find().sort("_id", 1))
    # Create a new list for holding the fully rendered issues to be sent to html.
    rendered_survey_issues = []
    # Loop through Mongo DB's returned list.
    for budgie in survey_issues:
        room_ref = budgie['roomRef']
        # Look up electricalRooms collection to get room type, description and voltage.
        room_dictionary = mongo.db.electricalRooms.find_one({"roomRef": room_ref})
        room_type = room_dictionary['roomType']
        room_desc = room_dictionary['roomDesc']
        room_volts = room_dictionary['roomVolts']
        # Look up surveyQuestions collection to get full question texts.
        question_no = budgie['questionNumber']
        question_dictionary = mongo.db.surveyQuestions.find_one({"questionNumber": question_no})
        question_short = question_dictionary['questionShort']
        question_long = question_dictionary['questionLong']
        # Get the comment added by the surveyor.
        issue_comment = budgie['issueComment']
        # Look up user collections to get the surveyor's full name and company 
        created_by = budgie['createdBy']
        created_by_dictionary = mongo.db.users.find_one({"username": created_by})
        created_by_fullname = created_by_dictionary['first_name'] + " " + created_by_dictionary['last_name']
        created_by_company = created_by_dictionary['company']
        # Convert date time stamp to full text formatting.
        created_at = budgie['createdAt'].strftime("%A, %d. %B %Y %I:%M%p")
        created_at_short = budgie['createdAt'].strftime("%d/%m/%y")
        # Pack all values into a dictionary and append it to the
        # rendered_survey_issues list.
        issue = {
            'roomRef': room_ref,
            'roomType': room_type,
            'roomDesc': room_desc,
            'roomVolts': room_volts,
            'questionNumber': question_no,
            'questionShort': question_short,
            'questionLong': question_long,
            'issueComment': issue_comment,
            'createdBy': created_by,
            'createdByFullname': created_by_fullname,
            'createdByCompany': created_by_company,
            'createdAt': created_at,
            'createdAtShort': created_at_short,
        }
        rendered_survey_issues.append(issue)
    # end testing code here testhigh ------------------------------------------
    rooms = list(mongo.db.electricalRooms.find().sort("_id", 1))
    questions = list(mongo.db.surveyQuestions.find().sort("_id", 1))
    voltages = list(mongo.db.voltages.find().sort("_id", 1))
    types = list(mongo.db.roomTypes.find().sort("_id", 1))
    return render_template("test-page.html", rendered_survey_issues=rendered_survey_issues,survey_issues=survey_issues, now=now, date_time_string=date_time_string, rooms=rooms, questions=questions, voltages=voltages, types=types)


@app.route("/user_list")
def user_list():
    """
    Render the user list.
    """
    return render_template("user-list.html")


# Main function
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
