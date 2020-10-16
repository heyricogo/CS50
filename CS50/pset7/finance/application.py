import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares, price_per_share, stock_name, total_price FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    user_id = session["user_id"]
    
    rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
    cash_remaining = rows[0]["cash"]
    
    return render_template("index.html", stocks=stocks, cash_remaining=cash_remaining)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        # Ensure symbol was submitted
        if quote == None:
            return apology("must provide a valid symbol", 400)
        # Ensure number of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide a number of shares", 403)
        # Check if shares was a positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Check if # of shares requested was 0
        if shares <= 0:
            return apology("can't buy less than or 0 shares", 400)
        current_price = quote["price"]
        stock_name = quote["name"]
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        
        # How much $ the user still has in her account
        cash_remaining = rows[0]["cash"]
        
        # Calculate the price of requested shares
        total_price = shares * current_price
        
        if total_price > cash_remaining:
            return apology("not enough cash")
        
        # update table in the database and insert transactions
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share, stock_name, total_price) VALUES(:user_id, :symbol, :shares, :price, :name, :total_price)", user_id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, price=current_price, name=stock_name, total_price=total_price)
        
        flash("Bought!")
        
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute(
        "SELECT symbol, shares, price_per_share, transacted FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])
    user_id = session["user_id"]
    
    return render_template("history.html", stocks=stocks)


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
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("invalid symbol", 400)
            
        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")
    
        
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) == 1:
            return apology("the username already exists", 400)
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)        
        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("the password and the confirmed password are different", 400)
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
        username=request.form.get("username"), hash=hash)
    
        # Remember the user log in
        session["user_id"] = new_user_id
        
        # Registered message
        flash("Registered!")

        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
        
 
@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change password of the user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure password was submitted
        if not request.form.get("oldPassword"):
            return apology("must provide password", 400)
        if not request.form.get("newPassword"):
            return apology("must provide password", 400)        
        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)
        if request.form.get("newPassword") != request.form.get("confirmation"):
            return apology("the new password and the confirmed password are different", 400)
        
        # Verify Old password
        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])
        oldHash = rows[0]["hash"]
        oldPassword = request.form.get("oldPassword")
        if not check_password_hash(oldHash, oldPassword):
            return apology("the old password is wrong", 400)
            
        # register new password and hash it
        hash = generate_password_hash(request.form.get("newPassword"))
        new_user_id = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash=hash)
        
        # Registered message
        flash("Password change!")

        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Take the username of the user
        rows = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])
        username = rows[0]["username"]
        
        return render_template("changePassword.html", username=username)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        # Ensure symbol was submitted
        if quote == None:
            return apology("must provide symbol", 403)
        # Ensure number of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide a number of shares", 403)
        # Check if shares was a positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Check if # of shares requested was 0
        if shares <= 0:
            return apology("can't buy less than or 0 shares", 400)
        
        current_price = quote["price"]
        stock_name = quote["name"]
        symbol = quote["symbol"]
        
        stocks = db.execute("SELECT SUM(shares) FROM transactions WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol", user_id=session["user_id"], symbol=symbol)
        user_id = session["user_id"]
        nb_shares = int(stocks[0]["SUM(shares)"])
        
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        cash_remaining = rows[0]["cash"]
        
        if shares > nb_shares:
            return apology("not enough shares")
        
        total_price = shares * current_price
        # update table in the database and insert transactions
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share, stock_name, total_price) VALUES(:user_id, :symbol, :shares, :price, :name, :total_price)", user_id=session["user_id"], symbol=symbol, shares=-shares, price=current_price, name=stock_name, total_price=total_price)
        
        flash("Sold!")
        
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0", user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
