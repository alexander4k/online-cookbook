from flask import Flask
from flask_pymongo import PyMongo

app = Flask("app")
    
app.config["MONGO_DBNAME"] = "online-cookbook"
app.config["MONGO_URI"] = "mongodb://admin:kawaii1010@ds259463.mlab.com:59463/online-cookbook"
    
mongo = PyMongo(app)
    