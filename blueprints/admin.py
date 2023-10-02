from flask import Blueprint, render_template, abort, request, redirect,session
import config

app = Blueprint("admin", __name__)


@app.route('/admin/login', methods=["POST", "GET"])
def login():  # put application's code here
    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session['admin_login'] = username
            return redirect("/admin/dashboard")
        else:
            return redirect("/admin/login")
    else:
        return render_template("/admin/login.html")

@app.route('/admin/dashboard', methods=["GET"])
def dashboard():  # put application's code here
    if session.get('admin_login', None) == None:
        abort(403)

    return "dashboard"

