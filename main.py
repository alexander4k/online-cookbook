import os
import time
from flask import Flask, render_template, request, redirect, url_for

from utils import app_setup, queries, misc


app = app_setup.app

@app.route("/")
def home():
    recent = queries.get_top_ten_descending("creation_date")
    most_popular = queries.get_top_ten_descending("votes")
    least_popular = queries.get_top_ten_ascending("votes")
    
    formatted_dates = queries.format_dates()
    
    return render_template("home.html",
                            most_popular=most_popular,
                            recent=recent,
                            least_popular=least_popular,
                            formatted_dates=formatted_dates)
    
@app.route("/add_recipe")
def add_recipe():
    cuisines = app_setup.mongo.db.recipes.distinct("cuisine")
    categories = app_setup.mongo.db.recipes.distinct("category")

    cuisines_capitalized = queries.return_capitalized_unique_items_in_list(cuisines)
    categories_capitalized = queries.return_capitalized_unique_items_in_list(categories)
    
    return render_template("add_recipe.html",
                            categories=categories_capitalized,
                            cuisines=cuisines_capitalized)
                            
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    if request.method == "POST":
        queries.insert_recipe(request.form.get("title"),
                           request.form.get("description"),
                           request.form.get("image"),
                           "temporary",
                           request.form.get("servings"),
                           request.form.get("cuisine"),
                           request.form.get("category"),
                           request.form.get("difficulty"),
                           request.form.get("prep_time"),
                           request.form.get("cook_time"),
                           request.form.get("calories"),
                           request.form.get("fat"),
                           request.form.get("saturates"),
                           request.form.get("carbs"),
                           request.form.get("sugars"),
                           request.form.get("salt"),
                           request.form.get("fibre"),
                           request.form.get("protein"),
                           request.form.getlist("allergen"),
                           filter(None, request.form.getlist("ingredient")),
                           filter(None, request.form.getlist("instruction")))
                           
    return redirect(url_for("add_recipe"))                   
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)