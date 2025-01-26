import os

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
    return render_template('forgot_password.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # TODO: IF the user is loged in revert to the dashboard

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = ...

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    return render_template("register.html")


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
