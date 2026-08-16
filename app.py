from flask import Flask, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route('/')
def home():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("home.html", products=products)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(id)
    session.modified = True
    return redirect('/')

@app.route('/cart')
def cart():
    db = get_db()
    items = []
    total = 0

    if "cart" in session:
        for i in session["cart"]:
            product = db.execute("SELECT * FROM products WHERE id=?", (i,)).fetchone()
            items.append(product)
            total += product[2]

    return render_template("cart.html", items=items, total=total)

@app.route('/order')
def order():
    session.pop("cart", None)
    return "Order Placed Successfully!"

if __name__ == '__main__':
    app.run(debug=True)
