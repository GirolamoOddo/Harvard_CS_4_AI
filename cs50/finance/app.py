import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, change_password

app = Flask(__name__)


app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()
    return redirect("/")


## implented routes ############################

# register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        hash = generate_password_hash(password)

        try:
            user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except ValueError:
            return apology("username already exists", 400)

        session["user_id"] = user_id

        return redirect("/")

    else:
        return render_template("register.html")


# quote
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        # lookup is used to get stock data
        stock = lookup(symbol)

        if stock is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


# buy
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive integer for shares", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        shares = int(shares)
        user_id = session["user_id"]

        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        total_cost = shares * stock["price"]

        if cash < total_cost:
            return apology("can't afford", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, shares, stock["price"])

        return redirect("/")

    else:
        return render_template("buy.html")

# index (user portfolio)


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = rows[0]["cash"]

    rows = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)
    stocks = []
    total_value = cash
    for row in rows:
        stock = lookup(row["symbol"])
        total = stock["price"] * row["total_shares"]
        total_value += total
        stocks.append({
            "symbol": row["symbol"],
            "shares": row["total_shares"],
            "price": stock["price"],
            "total": total
        })

    return render_template("index.html", cash=cash, stocks=stocks, total_value=total_value)

# sell


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive integer for shares", 400)

        shares = int(shares)
        user_id = session["user_id"]

        row = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        if len(row) != 1 or row[0]["total_shares"] < shares:
            return apology("not enough shares", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        total_value = shares * stock["price"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, stock["price"])

        return redirect("/")

    else:
        user_id = session["user_id"]
        rows = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in rows])

# history


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    rows = db.execute(
        "SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ? ORDER BY transacted DESC", user_id)

    return render_template("history.html", transactions=rows)

# extra: add money


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to user's account."""
    if request.method == "POST":

        if not request.form.get("amount"):
            return apology("must provide amount", 403)
        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                return apology("amount must be positive", 403)
        except ValueError:
            return apology("invalid amount", 403)

        user_id = session["user_id"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, user_id)

        flash(f"${amount:.2f} added to your account!")
        return redirect("/")
    else:
        return render_template("add_cash.html")


# extra: pw change
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user's password."""
    if request.method == "POST":

        if not request.form.get("old_password"):
            return apology("must provide old password", 403)

        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        if not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("invalid old password", 403)

        if not request.form.get("new_password"):
            return apology("must provide new password", 403)

        if not request.form.get("confirmation") or request.form.get("new_password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        new_password = request.form.get("new_password")
        change_password(user_id, new_password)

        flash("Password changed successfully!")
        return redirect("/")
    else:
        return render_template("change_password.html")
