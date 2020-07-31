import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd
# pk_246126e628204dff8966c9efcd761463
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    db.execute("CREATE TABLE IF NOT EXISTS 'own' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' INTEGER NOT NULL, 'stock' TEXT NOT NULL, 'shares' INTEGER NOT NULL, 'name' TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id));")
    stock_shares = db.execute("SELECT stock, shares, name FROM own WHERE user_id = :user_id;", user_id = session["user_id"])
    current = []
    length = len(stock_shares)

    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])[0]["cash"]
    for i in range(length):
        current.append(lookup(stock_shares[i]["stock"])["price"])
    total = cash
    for i in range(len(current)):
        total = total + current[i]*stock_shares[i]["shares"]
    return render_template("index.html", stock_shares = stock_shares, current = current, length=length, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if stock == None:
            return render_template("apology.html", message="No stock symbol was entered")
        if not request.form.get("shares"):
            return render_template("apology.html", message="No shares were entered")
        shares = float(request.form.get("shares"))
        if shares <= 0:
            return render_template("apology.html", message="Must enter positive number of shares to buy")
        current = db.execute("SELECT cash FROM users WHERE :userid = id", userid = session["user_id"])
        new = current[0]["cash"] - stock["price"] * shares
        if new < 0:
            return render_template("apology.html", message="Insufficient funds")
        else:
            now = datetime.now()
            db.execute("UPDATE users SET cash = :new WHERE :userid = id", new = new, userid = session["user_id"])
            db.execute("CREATE TABLE IF NOT EXISTS 'log' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' INTEGER NOT NULL, 'stock' TEXT NOT NULL, 'shares' INTEGER NOT NULL, 'price_bought' INTEGER, 'price_sold' INTEGER, 'bought' BIT, 'sold' BIT, 'time' TEXT, FOREIGN KEY(user_id) REFERENCES users(id));")
            db.execute("INSERT INTO log (user_id, stock, shares, price_bought, bought, time) VALUES (:user_id, :stock, :shares, :price_bought, :bought, :time)", user_id = session["user_id"], stock = stock["symbol"], shares = shares, price_bought = stock["price"], bought = 1, time=now)
            if len(db.execute("SELECT stock FROM own WHERE user_id = :user_id", user_id=session["user_id"])) > 0:
                if stock["symbol"] in db.execute("SELECT stock FROM own WHERE user_id = :user_id", user_id=session["user_id"])[0]["stock"]:
                    db.execute("UPDATE own SET shares=shares + :shares WHERE user_id=:user_id AND stock=:stock", shares=shares, user_id=session["user_id"], stock=stock["symbol"])
                else:
                    db.execute("INSERT INTO own (user_id, stock, shares, name) VALUES (:user_id, :stock, :shares, :name)", user_id=session["user_id"], stock=stock["symbol"], shares=shares, name=stock["name"])
                    print("else")
            else:
                # User has never bought a stock
                db.execute("INSERT INTO own (user_id, stock, shares, name) VALUES (:user_id, :stock, :shares, :name)", user_id=session["user_id"], stock=stock["symbol"], shares=shares, name=stock["name"])
            return redirect("/")

@app.route("/history")
@login_required
def history():
    stock_shares = db.execute("SELECT stock, shares, time, price_bought, price_sold, bought, sold FROM log WHERE user_id=:user_id", user_id=session["user_id"])
    length = len(stock_shares)
    stock = []
    shares = []
    time = []
    price = []
    for i in range(length):
        stock.append(stock_shares[i]["stock"])
        time.append(stock_shares[i]["time"])
        if stock_shares[i]["bought"] == 1:
            shares.append(stock_shares[i]["shares"])
            price.append(stock_shares[i]["price_bought"])
        else:
            shares.append(-1 * stock_shares[i]["shares"])
            price.append(stock_shares[i]["price_sold"])
    return render_template("history.html", length=length, stock=stock, shares=shares, time=time, price=price)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    else:
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        if password != confirm:
            return render_template("apology.html", message="Your passwords do not match")
        else:
            hashed = generate_password_hash(password)
            db.execute("UPDATE users SET hash = :hashed WHERE id=:user_id", hashed=hashed, user_id=session["user_id"])
            return redirect("/")

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if stock == None:
            return render_template("apology.html", message="No stock symbol was entered")
        else:
            return render_template("quoted.html", message = "A share of {} ({}) costs ${}.".format(stock["name"], stock["symbol"], stock["price"]))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return render_template("apology.html", message="You must enter a username")
        if username in db.execute("SELECT username FROM users"):
            return render_template("apology.html", message="That username is taken")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if not password:
            return render_template("apology.html", message="You must enter a password")
        if password != confirm:
            return render_template("apology.html", message="Your passwords do not match")
        else:
            hashed = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed)", username=username, hashed=hashed)
            return redirect("/login")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        return render_template("sell.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return render_template("apology.html", message="No symbol was entered")
        if lookup(symbol) == None:
            return render_template("apology.html", message="No valid stock symbol was entered")
        alls = []
        poop = db.execute("SELECT stock FROM own WHERE user_id = :user_id AND shares != 0;", user_id=session["user_id"])
        for i in range(len(poop)):
            alls.append(poop[i]["stock"])
        if symbol not in alls:
            return render_template("apology.html", message="You don't own this stock")
        if not request.form.get("shares"):
            return render_template("apology.html", message="No shares were entered")
        shares = float(request.form.get("shares"))
        if shares <= 0:
            return render_template("apology.html", message="Must be positive amount of shares")
        elif shares > db.execute("SELECT shares FROM own WHERE user_id = :user_id AND stock = :symbol", user_id=session["user_id"], symbol=symbol)[0]["shares"]:
            return render_template("apology.html", message="You don't own this many shares")
        else:
            now = datetime.now()
            value = lookup(symbol)["price"] * shares
            db.execute("UPDATE users SET cash = cash + :value WHERE id=:user_id", value=value, user_id=session["user_id"])
            db.execute("UPDATE own SET shares = shares - :shares WHERE stock = :symbol AND user_id=:user_id", shares=shares, symbol=symbol, user_id=session["user_id"])
            db.execute("INSERT INTO log (user_id, stock, shares, price_sold, sold, time) VALUES (:user_id, :stock, :shares, :price_sold, :sold, :time)", user_id=session["user_id"], stock=symbol, shares=shares, price_sold=lookup(symbol)["price"], sold=1, time=now)
            db.execute("DELETE FROM own WHERE shares = 0 AND user_id=:user_id", user_id=session["user_id"])
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
