import os
import chess
import chess.engine

from chessdotcom import get_current_daily_puzzle, get_leaderboards, get_player_profile, get_player_stats
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Create chess engine instance
engine = chess.engine.SimpleEngine.popen_uci("/engine/stockfish/stockfish-ubuntu-x86-64-sse41-popcnt")

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
    

@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    """Play chess"""
    
    # POST 
    if request.method == "POST":
        pass
    
    # GET
    else:
        return render_template("play.html")
    
    
@app.route("/engine_move", methods=["POST"])
def engine_move():
    """Chess engine move"""
    
    # Extract FEN string from HTTP POST request body
    fen = request.form.get('fen')
    
    # Initialize python chess board instance
    board = chess.Board(fen)
    
    # Engine move
    result = engine.play(board, chess.engine.Limit(time=0.1))
    
    # Update python chess board state
    board.push(result.move)
    
    # Extract FEN from current board state
    fen = board.fen()
    
    return {'fen': fen, 'best_move': str(result.move)}


@app.route("/puzzle", methods=["GET", "POST"])
@login_required
def puzzle():
    """Solve daily puzzle"""
    
    # POST
    if request.method == "POST":
        data = get_current_daily_puzzle().json
        puzzle = data["puzzle"]
        
        return {'fen': puzzle["fen"]}
    
    # GET
    else:
        data = get_current_daily_puzzle().json
        puzzle = data["puzzle"]
        return render_template("puzzle.html", puzzle=puzzle)
    
    
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


@app.route("/about")
def about():
    """Show about"""
    
    return render_template("about.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Show profile"""
    
    # POST
    if request.method == "POST":
        
        searched_username = request.form.get("username")
        try:
            data_profile = get_player_profile(searched_username).json
            data_stats = get_player_stats(searched_username).json
        except:
            error_message = "Invalid username"
            return render_template("search_profile.html", error_message=error_message)
        
        player = data_profile["player"]
        player["username"] = player["url"][-len(searched_username):]
        country = player["country"][-2:].lower()
        player["country"] = "-".join(("flag", country))
        player["status"] = player["status"].capitalize()
        
        stats = data_stats["stats"]
        
        categories = ["chess_blitz", "chess_bullet", "chess_rapid"]
        
        games = {}
        games["total"] = 0
        for category in categories:
            games[category] = 0
            try:
                for gameScenario in stats[category]["record"]:
                    games[category] += stats[category]["record"][gameScenario] 
                games["total"] += games[category]
            except:
                pass
            
        return render_template("profile.html", player=player, stats=stats, categories=categories, games=games)
    
    # GET
    else:
        return render_template("search_profile.html")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)