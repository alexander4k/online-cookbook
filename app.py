import os
from flask import Flask, render_template
from flask_pymongo import PyMongo

import db_connection

app = Flask(__name__)

app.config["MONGO_DBNAME"] = db_connection.dbname
app.config["MONGO_URI"] = db_connection.uri

mongo = PyMongo(app)

@app.route("/")
def hello():
    recipes = mongo.db.recipes.find()
    
    return render_template("home.html", recipes=recipes)
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)