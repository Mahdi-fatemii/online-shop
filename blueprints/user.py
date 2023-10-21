from flask import Blueprint, render_template, flash, url_for, request, redirect
from flask_login import login_user, login_required, current_user
from passlib.hash import sha256_crypt
import requests
from models.cart import Cart
from models.cart_item import CartItem
from models.payment import Payment
from models.product import Product
from models.user import User
from extentions import db
import config
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
        item.price = product.price
        item.cart = cart
        item.product = product
        db.session.add(item)
    else:
        cart_item.quantity += 1

    db.session.commit()

    return redirect(url_for('user.cart'))


@app.route('/remove-from-cart', methods=["GET"])
@login_required
def remove_from_cart():
    id = request.args.get('id')
    cart_item = CartItem.query.filter(CartItem.id == id).first_or_404()
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.session.delete(cart_item)

    db.session.commit()
    return redirect(url_for('user.cart'))


@app.route('/cart', methods=["GET"])
@login_required
def cart():
    cart = current_user.carts.filter(Cart.status == "pending").first()
    return render_template("/user/cart.html", cart=cart)


@app.route('/payment', methods=["GET"])
@login_required
def payment():
    cart = current_user.carts.filter(Cart.status == 'pending').first()

    r = requests.post(config.PAYMENT_FIRST_REQUEST_URL,
                      data={
                          'api': config.PAYMENT_MERCHANT,
                          'amount': cart.total_price(),
                          'callback': config.PAYMENT_CALLBACK,
                      })
    token = r.json()['result']['token']
    url = r.json()['result']['url']

    pay = Payment(price=cart.total_price(), token=token)
    pay.cart = cart
    db.session.add(pay)
    db.session.commit()

    return redirect(url)


@app.route('/verify', methods=["GET"])
@login_required
def verify():
    token = request.args.get('token')
    pay = Payment.query.filter(Payment.token == token).first_or_404()

    r = requests.post(config.PAYMENT_VERIFY_REQUEST_URL,
                      data={
                          'api': 'sandbox',
                          'amount': pay.price,
                          'token': token
                      })

    pay_status = bool(r.json()['success'])

    if pay_status:
        transaction_id = r.json()['result']['transaction_id']
        refid = r.json()['result']['refid']
        card_pan = r.json()['result']['card_pan']

        pay.card_pan = card_pan
        pay.transaction_id = transaction_id
        pay.refid = refid
        pay.status = 'success'
        pay.cart.status = 'purchased'
        flash('payment was successful')
    else:
        flash('payment was not successful')
        pay.status = 'failed'

    db.session.commit()

    return redirect(url_for('user.dashboard'))


@app.route('/user/dashboard', methods=["GET"])
@login_required
def dashboard():
        return render_template("/user/dashboard.html")


@app.route('/user/dashboard/order/<id>', methods=["GET"])
@login_required
def order(id):
    cart = current_user.carts.filter(Cart.id == id).first_or_404()
    return render_template("/user/order.html", cart=cart)
