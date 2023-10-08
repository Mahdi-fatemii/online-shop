from flask import Blueprint, render_template, flash, url_for, request, redirect
from flask_login import login_user
from passlib.hash import sha256_crypt
from models.user import User
from extentions import db
import models.user

app = Blueprint("user", __name__)


@app.route('/user/dashboard', methods=["GET"])
def dashboard():
    return render_template("/user/dashboard.html")


@app.route('/user/login/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template("user/signup.html")
    else:
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
            return redirect('/user/login/signup')

        user = User(username=username, password=sha256_crypt.encrypt(password), name=name,
                    lastName=lastName, phone=phone, email=email,address=address)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect("/user/login")


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = User.query.filter(User.username == username).first()
        if user is not None and sha256_crypt.verify(password, user.password) is True:
            login_user(user)
            return redirect("/user/dashboard")
        else:
            flash('invalid username or password')
            return redirect(url_for("user.user_login"))
    else:
        return render_template("user/login.html")
