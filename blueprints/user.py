from flask import Blueprint
import models.user

app = Blueprint("user", __name__)


@app.route('/user')
def user():  # put application's code here
    return 'this is user page'



