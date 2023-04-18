import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create connection to database
connection = sqlite3.connect("app.db", check_same_thread=False)
cursor = connection.cursor()

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
    if request.method == "POST":
        pass
    
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
        print(cursor.execute("SELECT * FROM users WHERE username = ?", [username]))
        print(cursor.fetchone())
        # elif  == True:
        #     return render_template("error.html", message="username is taken")
        
        # Remember user 
        cursor.execute("INSERT INTO users (username, hash) VALUES(?, ?)", [username, hash])
        connection.commit()
        
        # Query database for username 
        result = cursor.execute("SELECT * FROM users WHRE username = ?", [username])
        
        print(result.fetchone()) 
        
        # Remember which user has logged in
        session["user_id"] = result[0]["id"]
        
        flash("Registered!")
        
        return redirect("/")  
    
    # GET
    else:
        return render_template("register.html")