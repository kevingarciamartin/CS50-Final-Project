# Chess50
#### Deployment:  [Live website](https://chess50-dde8edd06871.herokuapp.com/)
#### Video Demo:  https://youtu.be/QW3ZiED2QSU
#### Description:
This is Chess50, my final project of the CS50x - Introduction to Computer Science course. It is a web-based mini-clone application of the popular website chess.com. The front-end is mainly made with HTML and CSS, with some JavaScript for interactivity. The back-end is a combination of Python and JavaScript as well as Flask as the framework and SQLite for databases.

Features include:
- playing chess against an engine (Stockfish 15.1) with take-back moves, engine moves on demand and flipping the board,
- solving chess.com's Daily Puzzle,
- keeping track of the leaderboards for the most popular time controls,
- and searching for valid chess.com usernames to get their profile information and game statistics.

### Engine
Includes two versions of the chess engine Stockfish 15.1, one slower than the other. I could not tell a defference between the two and chose the slower one as I deemed it good enough.

### static
Includes stylesheets, JavaScript and images.

#### css
Includes all of the stylesheets.

##### chessboard-1.0.0.min.css
A stylesheet from chessboardjs.com for customizing their chess board.

##### flags.css
A stylesheet with emoji country flags from https://github.com/AAKempf/emoji-country-flags for representing chess.com user's nationalities.

##### styles.css
The main stylesheet for the project.

#### img
Includes the images of the chess pieces.

#### js
Includes the JavaScript.

##### app.js
A script for toggeling the mobile menu.

##### chess.js 
A TypeScript chess library from https://github.com/jhlywa/chess.js for chess move generation/validation, piece placement/movement, and check/checkmate/draw detection.

##### chessboard-1.0.0.min.js
A script from chessboardjs.com for embedding a chessboard on a site.

### templates
Includes the html templates. I decided on making a layout template for the overarching structure of the website where all the other templates would be called.

#### layout.html
The main template with the page title, packages and the menues - unfortunately, due to inexperience with media queries, I made separate menues for mobile and desktop in the markup. The appropiate template is rendered with block elements.

#### play.html
The template for playing chess against the chess engine (Stockfish 15.1).

#### puzzle.html
The template for solving chess.com's Daily Puzzle.

#### leaderboard.html
The template for showing the top five leaderboards of the most popular time controls on chess.com.

#### search_profile.html
The template for searching chess.com usernames.

#### profile.html
The template for showing chess.com user's profile information and game statistics.

#### about.html
The template for showing brief information about the website.

#### register.html
The template for registering a new Chess50 account.

#### login.html
The template for logging into Chess50.

#### error.html
The template for showing error messages. This template did not get enough time or care.

### app.db
An SQL database of the Chess50 accounts with hashed passwords.

### schema.sql
The SQL database schema.

### app.py
A Python script that renders/redirects the user between different templates, makes API requests, runs the chess engine and handles user sessions.

### helpers.py
Decorates routes to require login.

### .gitignore
Ignores files.

### requirements.txt
A file that stores information about all the libraries, modules, and packages specific to the project.
