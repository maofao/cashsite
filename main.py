from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "wiyazmkid1e"  #ключ для работы сессий

# продукт
products = [
    {"id": 1, "name": "Телефон", "price": 500},
    {"id": 2, "name": "Ноутбук", "price": 1000},
    {"id": 3, "name": "Наушники", "price": 100},
]

@app.before_request
def reset_cart_on_new_session():
    if "cart_initialized" not in session:
        session["cart"] = []  # сбрасываем
        session["cart_initialized"] = True  # флаг

# глав страница
@app.route("/")
def home():
    return render_template("home.html", products=products)

# добавление в корзину
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []

    for product in products:
        if product["id"] == product_id:
            session["cart"].append(product)
            break

    session.modified = True
    return redirect(url_for("home"))

#  корзина
@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total=total)

#  читска корзины вручную
@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)  # сброс корзины из сессии
    return redirect(url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True)
