from flask import Blueprint

app = Blueprint("admin", __name__)


@app.route('/admin')
def admin():  # put application's code here
    return 'this is admin page'



