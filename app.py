from flask import Flask, redirect, url_for, flash
# connecting blueprints
from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user
from blueprints.product import app as product
# adding CSRFProtect
from flask_wtf.csrf import CSRFProtect
# adding configs
import config
# adding database
import extentions
from flask_login import LoginManager
from models.user import User
# registering blueprints
app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(product)
# database configs
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
extentions.db.init_app(app)
# CSRFProtect
csrf = CSRFProtect(app)
# user login manager
login_manager = LoginManager()
login_manager.init_app(app)

# user login manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    flash('please login to your account first')
    return redirect(url_for('user.user_login'))

# database creation


with app.app_context():
    extentions.db.create_all()


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
