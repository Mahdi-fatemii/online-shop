SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
SECRET_KEY = "D4545aer54fe2afF544wre654gdf5aw4e51fs"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

PAYMENT_MERCHANT = "sandbox"
PAYMENT_CALLBACK = "http://localhost:5000/verify"
PAYMENT_FIRST_REQUEST_URL = 'https://sandbox.shepa.com/api/v1/token'
PAYMENT_VERIFY_REQUEST_URL = 'https://sandbox.shepa.com/api/v1/verify'
