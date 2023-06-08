import os

from chessdotcom import get_leaderboards
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create connection to database
db = SQL("sqlite:///app.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Home page"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()
    
    # POST
    username = request.form.get("username")
    password = request.form.get("password")
    
    if request.method == "POST":
        
        # Ensure username was submitted
        if not username:
            return render_template("error.html", message="must provide username")
        
        # Ensure password was submitted
        elif not password:
            return render_template("error.html", message="must provide password")
        
        # Query database for username 
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("error.html", message="invalid username and/or password")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")
            
    # GET
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""
    
    # Forget any user_id
    session.clear()
    
    return redirect("/")
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # POST 
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)
        
        # Ensure username was submitted
        if not username:
            return render_template("error.html", message="must provide username")
        
        # Ensure password was submitted
        elif not password:
            return render_template("error.html", message="must provide password")
        
        # Ensure password confirmation was submitted
        elif not confirmation:
            return render_template("error.html", message="must provide password confirmation")
        
        # Ensure password and confirmation match
        elif password != confirmation:
            return render_template("error.html", message="passwords don't match")
        
        # Ensure username doesn't exist
        if len(db.execute("SELECT * FROM users WHERE username = ?", username)) != 0:
            return render_template("error.html", message="username is taken")

        # Remember user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
 
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        flash("Registered!")
        
        return redirect("/")  
    
    # GET
    else:
        
        
        
        return render_template("register.html")
    

@app.route("/statistics", methods=["GET", "POST"])
@login_required
def statistics():
    """Show statistics"""
    
    # POST
    if request.method == "POST":
        pass
    
    # GET
    else:
        return render_template("statistics.html")
    
    
@app.route("/leaderboard", methods=["GET", "POST"])
@login_required
def leaderboards():
    """Show leaderboards"""
    
    # POST
    if request.method == "POST":
        pass
    
    # GET
    else:
        data = get_leaderboards().json
        leaderboards = data["leaderboards"]
        categories = ["live_blitz", "live_bullet", "live_rapid"]
        topfive = {}
        
        for category in categories:
            topfive[category] = leaderboards[category][0:5]
            
        return render_template("leaderboard.html", leaderboards=topfive, categories=categories)
    
@app.route("/about", methods=["GET"])
def about():
    """Show about"""
    
    return render_template("about.html")