import os
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "online-cookbook"
app.config["MONGO_URI"] = "mongodb://admin:kawaii1010@ds259463.mlab.com:59463/online-cookbook"

mongo = PyMongo(app)

@app.route("/")
def hello():
    recipes = mongo.db.recipes.find()
    
    return render_template("home.html", recipes=recipes)
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)