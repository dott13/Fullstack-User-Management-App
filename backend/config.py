from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/UserDb"

mongo = PyMongo(app)