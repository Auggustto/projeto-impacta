from flask import Flask, render_template, request, redirect, url_for, flash
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect

from app import app
from app.services.products import ProductsServices
from app.database.engine import get_connection

conn = get_connection()
products = ProductsServices(conn)
csrf = CSRFProtect(app)

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

@app.route("/", methods=["GET"])
def index():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email == "admin@teste.com" and password == "123456":
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("get"))
        else:
            flash("Email ou senha incorretos.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)

@app.route('/list_products', methods=['GET'])
def get():
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
        return redirect(url_for("get"))

    return render_template("register_products.html", product=product_data)

@app.route("/product/delete/<int:id>", methods=["POST"])
def delete(id):
    products.delete_product(id)
    return redirect(url_for("get"))