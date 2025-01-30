import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, is_eligible, image_to_text, text_to_image

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/set-theme', methods=['POST'])
def set_theme():
    data = request.get_json()
    session['theme'] = data.get('theme', 'light')
    return jsonify({'status': 'success'})


@app.route("/")
def index():
    """Show portfolio of stocks"""
    return render_template('home.html')


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """Look for the missing one or share about the one you found"""
    return apology("TODO")


@app.route('/legal-and-faq')
def legal_and_faq():
    return render_template('legal_and_faq.html')


@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')


@app.route('/forgot-password')
def forgot_password():
    
    # If the user is loged in redirect to the home
    if session.get("user_id") is not None:
        return redirect("/")
    
    return render_template('forgot_password.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # If the user is loged in redirect to the home
    if session.get("user_id") is not None:
        return redirect("/")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        data = {
            "national_id": request.form.get("national_id"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "birthday": request.form.get("birthday"),
            "password": request.form.get("password")
        }
        
        # Check required fields
        for field in data.keys():
            if not data[field]:
                flash(f"{field.replace('_', ' ').title()} is required")
                return render_template("login.html", values=data)

        # Ensure national ID number was submitted
        if not data["national_id"].isdigit() or len(data["national_id"]) != 14:
            flash("Invalid national id")
            return render_template("login.html", values=data)

        # Query database for username and national ID number
        data["username"] = data["first_name"].strip().title() + "_" + data["last_name"].strip().title() + "_" + data["national_id"]
        rows = db.execute( "SELECT * FROM Users WHERE username = ?", data["username"])

        if not is_eligible(data["national_id"], data["birthday"]):
            flash("Invalid Credentials")
            return render_template("login.html", values=data)

        # Ensure username, national ID, and birthday exist and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], request.form.get("password")
        ):
            flash("Invalid Credentials")
            return render_template("login.html", values=data)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # If the user is loged in redirect to the home
        if session.get("user_id") is not None:
            return redirect("/")

        data = {
            "national_id": "",
            "username": "",
            "birthday": "",
            "password": ""
        }

        return render_template("login.html", values=data)


@app.route("/logout")
def logout():
    """Log user out"""

    theme = session['theme']

    # Forget any user_id
    session.clear()
    
    session['theme'] = theme

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If the user is submiting the form
    if request.method == "POST":
        data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "national_id": request.form.get("national_id"),
            "id_front": request.files.get("id_front"),
            "id_back": request.files.get("id_back"),
            "birthday": request.form.get("birthday"),
            "address": request.form.get("address"),
            "phone_number": request.form.get("phone_number"),
            "password": request.form.get("password"),
            "confirm_password": request.form.get("confirm_password")
        }

        # Check required fields
        for field in data.keys():
            if not data[field]:
                print(data[field])
                flash(f"{field.replace('_', ' ').title()} is required")
                return render_template("register.html", values=data)

        # Ensure national ID number was submitted
        if not data["national_id"].isdigit() or len(data["national_id"]) != 14:
            flash("Invalid national id")
            return render_template("login.html", values=data)

        # Validate phone number format
        if not re.match(r'^\+20(10|11|12|15)\d{8}$', data["phone_number"]):
            flash("Invalid phone number format. Must start with +20 followed by 10, 11, 12, or 15 and 8 more digits.")
            return render_template("register.html", values=data)

        # Validate password strength
        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters")
            return render_template("register.html", values=data)
        
        if not re.search(r'[A-Z]', data["password"]):
            flash("Password must contain at least one uppercase letter")
            return render_template("register.html", values=data)
        
        if not re.search(r'[0-9]', data["password"]):
            flash("Password must contain at least one number")
            return render_template("register.html", values=data)
        
        if not re.search(r'[!@#$%^&*()_+{}|:"<>?~`-]', data["password"]):
            flash("Password must contain at least one special character")
            return render_template("register.html", values=data)

        # Check if confirm_password matches password
        if data["confirm_password"] != data["password"]:
            flash("Passwords do not match")
            return render_template("register.html", values=data)

        data["username"] = data["first_name"].strip().title() + "_" + data["last_name"].strip().title() + "_" + data["national_id"]
        rows = db.execute( "SELECT * FROM Users WHERE username = ?", data["username"])

        if len(rows) != 0:
            flash("The associated data is linked to a separate account")
            return render_template("register.html", values=data)

        db.execute(
            "INSERT INTO Users (national_id_number, username, first_name, last_name, birthday, address, phone_number, password_hash, national_id_front, national_id_back, theme) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                data["national_id"],
                data["username"],
                data["first_name"],
                data["last_name"],
                data["birthday"],
                data["address"],
                data["phone_number"],
                generate_password_hash(data["password"]),
                image_to_text(data["id_front"]),
                image_to_text(data["id_back"]),
                session['theme']
        )

        return redirect("/login")
    else:
        # If the user is loged in redirect to the home
        if session.get("user_id") is not None:
            return redirect("/")

        data = {
            "first_name": "",
            "last_name": "",
            "national_id": "",
            "id_front": "",
            "id_back": "",
            "birthday": "",
            "address": "",
            "phone_number": "",
            "password": "",
            "confirm_password": ""
        }

        return render_template("register.html", values=data)


@app.route('/about')
def about():
    team = [
        {
            "name": "Abdelrahman Ahmed Zain",
            "phone": "+201116904255",
            "email": "200047837@must.edu.eg",
            "image_url": "/static/images/abdelrahman.jpg"
        },
        {
            "name": "Assem Mohamed Saad",
            "phone": "+201278785473",
            "email": "200030013@must.edu.eg",
            "image_url": "/static/images/assem.jpg"
        },
        {
            "name": "Toqa Mohamed Omar",
            "phone": "+201016398628",
            "email": "200024268@must.edu.eg",
            "image_url": "/static/images/toqa.jpg"
        }
    ]

    return render_template('about.html', team=team)
