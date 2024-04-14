import os

from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import pytz

from helpers import apology, login_required

app = Flask(__name__)

db = SQL("sqlite:///time_zone.db")

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

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/timezone", methods=["GET", "POST"])
@login_required
def timezone():
    try:
        ytz = db.execute("select timezone from timezones")
    except:
        return apology("db error", 400)
    if request.method == "POST":
        yourtz = request.form.get("ytz")
        friendtz = request.form.get("ftz")

        if not yourtz or not friendtz:
            return apology("must select your and friend's timezone", 400)
        return render_template("timezone.html", ytz=ytz)
    return render_template("timezone.html", ytz=ytz)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

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

@app.context_processor
def global_var():
    try:
        username = db.execute("select username from users where id = ?", session["user_id"])
    except:
        username = [{'username':''}]
    return dict(user=username[0]['username'])

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/roman")
@login_required
def roman():
    res = []

    q = request.args.get("q")
    if q:
        for i in q:
            isup = False
            if i.isupper():
                isup = True
            letter = db.execute("SELECT en FROM letters WHERE ru = ?", i.lower())
            if letter:
                if isup:
                    res.append(letter[0]["en"].upper())
                else:
                    res.append(letter[0]["en"])
            else:
                res.append(i)
    return render_template("roman.html", res="".join(res))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        exist = db.execute(
            "SELECT count(username) AS cnt FROM users WHERE username = ?", name
        )

        if not name:
            return apology("must provide username", 400)
        elif exist[0]["cnt"] != 0:
            return apology("username is already taken", 400)

        pass1 = request.form.get("password")
        pass2 = request.form.get("confirmation")

        if not pass1 or not pass2:
            return apology("must provide password and confirmation", 400)
        elif len(pass1) < 8:
            return apology("must provide password with 8 characters minimum", 400)
        elif pass1 != pass2:
            return apology("password and confirmation should be the same", 400)

        db.execute(
            "INSERT INTO users (username, hash) VALUES(?,?)",
            name,
            generate_password_hash(pass1),
        )
        return redirect("/login")
    return render_template("/register.html")
