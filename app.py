from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecret"

# Fake user store (in memory)
users = {}

# Products (still hardcoded for now)
products = [
    {"id": 1, "name": "Laptop", "price": 500},
    {"id": 2, "name": "Phone", "price": 200},
    {"id": 3, "name": "Headphones", "price": 50}
]

# Cart (in session)
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        if username in users:
            return "User already exists. Please login."
        users[username] = {"cart": []}
        session["username"] = username
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        if username in users:
            session["username"] = username
            return redirect(url_for("index"))
        return "User not found. Please register first."
    return render_template("login.html")

@app.route("/index")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", products=products, username=session["username"])

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    for product in products:
        if product["id"] == product_id:
            users[username]["cart"].append(product)
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    return render_template("cart.html", cart=users[username]["cart"], username=username)

@app.route("/checkout")
def checkout():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    cart = users[username]["cart"]
    total = sum(item["price"] for item in cart)
    users[username]["cart"] = []  # empty cart after checkout
    return render_template("checkout.html", total=total, username=username)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("landing"))

if __name__ == "__main__":
    app.run(debug=True)
