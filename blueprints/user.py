from flask import Blueprint, render_template, abort, url_for, request, redirect, session
import config
from flask_login import login_user
from passlib.hash import sha256_crypt
from models.user import User
from extentions import db
import models.user

app = Blueprint("user", __name__)


# @app.before_request
# def before_request():
#     if session.get('user_login', None) == None and request.endpoint != "user.login":
#         abort(403)

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if User.query.filter(username == username and password == sha256_crypt.encrypt(password)):
            # session['user_login'] = username
            return redirect("/user/dashboard")
        else:
            return redirect("/user/login")
    else:
        return render_template("user/login.html")


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

        user = User(username=username, password=sha256_crypt.encrypt(password), name=name, lastName=lastName,
                    phone=phone, email=email,
                    address=address)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect("/user/login")
