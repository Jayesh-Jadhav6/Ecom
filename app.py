from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data
users = {}
products = {
    1: {"name": "Laptop", "price": 70000},
    2: {"name": "Phone", "price": 25000},
    3: {"name": "Headphones", "price": 3000}
}
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
    total = sum(p["price"] for p in cart)
    return render_template('cart.html', username=username, cart=cart, total=total)

# ----------------------------
# Checkout Page
# ----------------------------
@app.route('/checkout/<username>', methods=['GET', 'POST'])
def checkout(username):
    global order_counter
    if username not in users:
        return f"User not found. <a href='/'>Go back</a>"
    cart = users[username]["cart"]
    if not cart:
        return f"Cart is empty. <a href='/'>Go back</a>"
    
    total = sum(p["price"] for p in cart)
    
    if request.method == 'POST':
        orders[order_counter] = {"user": username, "items": cart}
        users[username]["cart"] = []
        order_counter += 1
        return f"Order placed successfully! <a href='/'>Home</a>"
    
    return render_template('checkout.html', username=username, cart=cart, total=total)

# ----------------------------
# Run App
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
