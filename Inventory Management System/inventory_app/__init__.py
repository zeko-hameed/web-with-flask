from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


from flask_wtf.csrf import CSRFProtect 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjkfisj893748923hrfeifwejf'
app.config['WTF_CSRF_ENABLED'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost:5432/inventory-db"


csrf = CSRFProtect(app) 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from inventory_app import routes