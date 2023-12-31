from flask import Blueprint, render_template, request

from models.product import Product

app = Blueprint("general", __name__)


@app.route('/')
def main():
    search = request.args.get('search', None)

    products = Product.query.filter(Product.status == 1)

    if search is not None:
        products = products.filter(Product.name.like(f'%{search}%'))

    products = products.all()

    return render_template("main.html", products=products, search=search)


@app.route('/product/<int:id>/<name>')
def product(id, name):
    product = Product.query.filter(Product.id == id).filter(Product.name == name).filter(
        Product.status == 1).first_or_404()
    return render_template('product.html', product=product)


@app.route('/about')
def about():
    return render_template("about.html")
