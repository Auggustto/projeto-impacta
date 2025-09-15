from flask import Flask, render_template, request, redirect, url_for

from app import app
from app.services.products import ProductsServices
from app.database.engine import get_connection

conn = get_connection()
products = ProductsServices(conn)

@app.route('/', methods=['GET'])
def index():
    result = products.list_all_products()
    return render_template("list_products.html", products=result)

@app.route("/product", methods=["GET", "POST"])
@app.route("/product/<int:id>", methods=["GET", "POST"])
def post(id=None):
    """
    Handles both creating a new product and editing an existing one.
    """
    product_data = None
    if id:
        product_data = products.get_product_by_id(id)

    if request.method == "POST":
        if id:
            products.update_product(id, request)
        else:
            products.register_products(request)
        return redirect(url_for("index"))

    return render_template("register_products.html", product=product_data)

@app.route("/product/delete/<int:id>", methods=["POST"])
def delete(id):
    products.delete_product(id)
    return redirect(url_for("index"))