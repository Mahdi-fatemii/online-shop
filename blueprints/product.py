from flask import Blueprint
import models.product

app = Blueprint("product", __name__)


@app.route('/product')
def product():  # put application's code here
    return 'this is product page'


