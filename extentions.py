import time
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def get_current_time():
    return round(time.time())
