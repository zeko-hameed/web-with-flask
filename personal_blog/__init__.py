from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = 'e053ce5bc93a6c14c4542e430caf9a9f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/P-Blog-db'
db = SQLAlchemy(app)


from personal_blog import route