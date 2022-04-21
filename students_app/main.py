from flask import Flask
import os
from dotenv import find_dotenv, load_dotenv

from .models import *

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    print(os.environ.get("DATABASE_URI"))
    return "s"
