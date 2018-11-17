import os
import time
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId

from utils import app_setup, queries, misc


app = app_setup.app

@app.route("/")
def home():
    recent = queries.get_top_ten_descending("creation_date")
    most_popular = queries.get_top_ten_descending("votes")
    least_popular = queries.get_top_ten_ascending("votes")
    
    formatted_dates = queries.format_dates(queries.get_top_ten_descending("creation_date"))
    
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
    
@app.route("/recipe_details/<recipe_id>")
def recipe_details(recipe_id):
    recipe = app_setup.mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    converted_creation_date = queries.format_date(recipe["creation_date"])
    time = recipe["time"]
    nutrition_values = queries.list_values(recipe["nutritional"])
    nutrition_names = sorted(misc.convert_items_in_list_to_capitalized(recipe["nutritional"]))
    return render_template("recipe_details.html",
                            recipe=recipe,
                            creation_date=converted_creation_date,
                            time=time,
                            nutrition_values=nutrition_values,
                            nutrition_names=nutrition_names)
                            
@app.route("/add_vote/<recipe_id>")
def add_vote(recipe_id):
    app_setup.mongo.db.recipes.update_one({"_id" : ObjectId(recipe_id)}, {"$inc": { "votes": 1}})
    
    return redirect(url_for("recipe_details", recipe_id=recipe_id))
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)