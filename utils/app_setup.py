import os
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

"""
Setup the app
"""

# Read from .env file and add to environment variable
load_dotenv(dotenv_path="secret_settings/.env")

app = Flask("main")
    
app.config["MONGO_DBNAME"] = os.getenv("DBNAME", 'defualt_dbname')
app.config["MONGO_URI"] = os.getenv("URI", 'default_uri')

SECRET_KEY = os.getenv("SECRET_KEY", '123456789')
app.secret_key = SECRET_KEY.encode("utf-8")
    
mongo = PyMongo(app)
    