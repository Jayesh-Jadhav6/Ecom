from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

# In-memory data
users = {}
products = {
    1: {"name": "Laptop", "price": 70000},
    2: {"name": "Phone", "price": 25000},
    3: {"name": "Headphones", "price": 3000}
}
carts = {}
orders = {}
order_counter = 1

# ----------------------------
# Homepage
# ----------------------------
@app.route('/')
def home():
    return render_template('index.html', products=products)

# ----------------------------
# User Registration
# ----------------------------
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    if username in users:
        return f"User {username} already exists. <a href='/'>Go back</a>"
    users[username] = {"cart": []}
    return f"User {username} registered! <a href='/'>Go back</a>"

# ----------------------------
# Add to Cart
# ----------------------------
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    username = request.form.get("username")
    product_id = int(request.form.get("product_id"))
    
    if username not in users:
        return f"User not found. <a href='/'>Go back</a>"
    if product_id not in products:
        return f"Product not found. <a href='/'>Go back</a>"
    
    users[username]["cart"].append(products[product_id])
    return redirect(url_for('view_cart', username=username))

# ----------------------------
# View Cart
# ----------------------------
@app.route('/cart/<username>')
def view_cart(username):
    if username not in users:
        return f"User not found. <a href='/'>Go back</a>"
    cart = users[username]["cart"]
    return f"<h2>{username}'s Cart</h2>" + "<br>".join([f"{p['name']} - ₹{p['price']}" for p in cart]) + \
           f"<br><br><a href='/'>Home</a> | <a href='/order/{username}'>Place Order</a>"

# ----------------------------
# Place Order
# ----------------------------
@app.route('/order/<username>')
def place_order(username):
    global order_counter
    if username not in users:
        return f"User not found. <a href='/'>Go back</a>"
    
    cart_items = users[username]["cart"]
    if not cart_items:
        return f"Cart is empty. <a href='/'>Go back</a>"
    
    orders[order_counter] = {"user": username, "items": cart_items}
    users[username]["cart"] = []
    order_counter += 1
    return f"Order placed successfully! <a href='/'>Go back</a>"

# ----------------------------
# Run App
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
