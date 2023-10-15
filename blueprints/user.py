from flask import Blueprint, render_template, flash, url_for, request, redirect
from flask_login import login_user, login_required, current_user
from passlib.hash import sha256_crypt

from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from models.user import User
from extentions import db
import models.user

app = Blueprint("user", __name__)


@app.route('/user/login/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template("user/signup.html")
    else:
        register = request.form.get('register', None)
        username = request.form.get('username', None)
        name = request.form.get('name', None)
        lastName = request.form.get('lastName', None)
        phone = request.form.get('phone', None)
        email = request.form.get('email', None)
        address = request.form.get('address', None)
        password = request.form.get('password', None)

        user = User.query.filter(User.username == username).first()
        if user is not None:
            flash('sorry this username is already taken by another person')
            return redirect(url_for('user.user_signup'))
        if register is not None:
            user = User(username=username, password=sha256_crypt.encrypt(password), name=name,
                        lastName=lastName, phone=phone, email=email,address=address)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('user.user_login'))


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = User.query.filter(User.username == username).first()
        if user is not None and sha256_crypt.verify(password, user.password) is True:
            login_user(user)
            return redirect(url_for('user.dashboard'))
        else:
            flash('invalid username or password')
            return redirect(url_for("user.user_login"))
    else:
        return render_template("user/login.html")


@app.route('/add-to-cart', methods=["GET"])
@login_required
def add_to_cart():
    id = request.args.get('id')
    product = Product.query.filter(Product.id == id).first_or_404()

    cart = current_user.carts.filter(Cart.status == 'pending').first()
    if cart is None:
        cart = Cart()
        current_user.carts.append(cart)
        db.session.add(cart)

    cart_item = cart.cart_items.filter(CartItem.product == product).first()
    if cart_item is None:
        item = CartItem(quantity=1)
        item.cart = cart
        item.product = product
        db.session.add(item)
    else:
        cart_item.quantity += 1

    db.session.commit()

    return redirect(url_for('user.cart'))


@app.route('/cart', methods=["GET", "POST"])
@login_required
def cart():
    return render_template("/user/cart.html")


@app.route('/user/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "GET":
        return render_template("/user/dashboard.html")
    else:
        return "this is a dashboard page"