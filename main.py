import os
import time
from flask import Flask, render_template, request, redirect, url_for, session
from bson.objectid import ObjectId

from utils import app_setup, queries, misc, sessions


app = app_setup.app

app.secret_key = os.urandom(16)

@app.route("/", methods=["GET", "POST"])
def index():
    users = app_setup.mongo.db.users.find()
    login_error = False
    
    if request.method == "POST":
        session.pop("user", None)
        for user in users:
            if request.form.get("password") == user["password"]:
                session["user"] = request.form.get("username")
                return redirect(url_for("index"))
            else:
                login_error = True
    
    username = None
    user = []
    user_favourites = []
    
    if "user" in session:
        username = sessions.check_if_user_in_session()
        user = app_setup.mongo.db.users.find_one({"username": username})
        user_favourites = user["favourite_recipes"]
        
    most_popular = queries.get_top_ten_descending("favourited")
    recent = queries.get_top_ten_descending("creation_date")
    oldest = queries.get_top_ten_ascending("creation_date")
    
    popular_dates = queries.format_dates(queries.get_top_ten_descending("favourited"))
    recent_dates = queries.format_dates(queries.get_top_ten_descending("creation_date"))
    oldest_dates = queries.format_dates(queries.get_top_ten_ascending("creation_date"))
    
    return render_template("index.html",
                            recent=recent,
                            most_popular=most_popular,
                            oldest=oldest,
                            popular_dates=popular_dates,
                            recent_dates=recent_dates,
                            oldest_dates=oldest_dates,
                            username=username,
                            user_favourites=user_favourites,
                            login_error=login_error)
                            
@app.route("/logout")
def logout():
    session.pop("user", None)
    
    return redirect(url_for("index"))
    
@app.route("/register_user")
def register_user():
    session.pop("user", None)
    
    return render_template("register.html")
    
@app.route("/insert_user", methods=["POST"])
def insert_user():
    queries.insert_user(request.form.get("username"),
                        request.form.get("password"))
    session["user"] = request.form.get("username")
    return redirect(url_for("index"))
    
@app.route("/account")
def account():
    formatted_dates = queries.format_dates(app_setup.mongo.db.recipes.find())
    recipes = app_setup.mongo.db.recipes.find()
    recipes_another = app_setup.mongo.db.recipes.find()
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    user_another = app_setup.mongo.db.users.find_one({"username": username})

    return render_template("account.html",
                            recipes=recipes,
                            recipes_another=recipes_another,
                            user_another=user_another,
                            user=user,
                            dates=formatted_dates)
    
@app.route("/add_recipe")
def add_recipe():
    username = sessions.check_if_user_in_session()
    cuisines = app_setup.mongo.db.recipes.distinct("cuisine")
    categories = app_setup.mongo.db.recipes.distinct("category")
    cuisines_capitalized = queries.return_capitalized_unique_items_in_list(cuisines)
    categories_capitalized = queries.return_capitalized_unique_items_in_list(categories)
    
    return render_template("add_recipe.html",
                            categories=categories_capitalized,
                            cuisines=cuisines_capitalized,
                            username=username)
                            
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    username = sessions.check_if_user_in_session()
    app_setup.mongo.db.users.update_one({"username": username}, {"$addToSet": {"my_recipes": request.form.get("title")}})
    
    if request.method == "POST":
        new_recipe = queries.create_recipe(request.form.get("title"),
                                           request.form.get("description"),
                                           request.form.get("image"),
                                           username,
                                           request.form.get("servings"),
                                           0,
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
        app_setup.mongo.db.recipes.insert_one(new_recipe)
                           
    return redirect(url_for("account")) 
    
@app.route("/edit_recipe/<recipe_title>")
def edit_recipe(recipe_title):
    username = sessions.check_if_user_in_session()
    recipe = app_setup.mongo.db.recipes.find_one({"title": recipe_title})
    recipe = app_setup.mongo.db.recipes.find_one({"title": recipe_title})
    cuisines = app_setup.mongo.db.recipes.distinct("cuisine")
    categories = app_setup.mongo.db.recipes.distinct("category")
    cuisines_capitalized = queries.return_capitalized_unique_items_in_list(cuisines)
    categories_capitalized = queries.return_capitalized_unique_items_in_list(categories)
    
    return render_template("edit_recipe.html",
                            recipe=recipe,
                            categories=categories_capitalized,
                            cuisines=cuisines_capitalized,
                            username=username)
                            
@app.route("/update_recipe/<recipe_title>", methods=["POST"])
def update_recipe(recipe_title):
    username = sessions.check_if_user_in_session()
    current_recipe = app_setup.mongo.db.recipes.find_one({"title": recipe_title})
    current_favourited_score = current_recipe["favourited"]
    
    new_recipe = queries.create_recipe(request.form.get("title"),
                                    request.form.get("description"),
                                    request.form.get("image"),
                                    username,
                                    request.form.get("servings"),
                                    current_favourited_score,
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
                                    
    app_setup.mongo.db.recipes.replace_one({"title": recipe_title}, new_recipe)
    app_setup.mongo.db.users.update_one({"username": username, "my_recipes": recipe_title}, {"$set": {"my_recipes.$": request.form.get("title")}})
    
    return redirect(url_for("recipe_details", recipe_title=request.form.get("title")))
    
@app.route("/delete_recipe/<recipe_title>")
def delete_recipe(recipe_title):
    app_setup.mongo.db.recipes.delete_one({"title": recipe_title})
    
    return redirect(url_for("account"))
    
@app.route("/recipe_details/<recipe_title>")
def recipe_details(recipe_title):
    username = None
    user_favourites = []
    recipe = app_setup.mongo.db.recipes.find_one({"title": recipe_title})
    converted_creation_date = queries.format_date(recipe["creation_date"])
    time = recipe["time"]
    nutritional = recipe["nutritional"]
    nutrition_names = []
    nutrition_values = []
    for name, value in nutritional.items():
        nutrition_names.append(name)
        nutrition_values.append(value)
    
    if "user" in session:
        username = sessions.check_if_user_in_session()
        user = app_setup.mongo.db.users.find_one({"username": username})
        user_favourites = user["favourite_recipes"]
    
    return render_template("recipe_details.html",
                            recipe=recipe,
                            creation_date=converted_creation_date,
                            time=time,
                            nutrition_names=nutrition_names,
                            nutrition_values=nutrition_values,
                            username=username,
                            user_favourites=user_favourites)
                            
@app.route("/favourite/<recipe_title>/<page>")
def favourite(recipe_title, page):
    username = None
    
    if "user" in session:
        username = session["user"]
        user = app_setup.mongo.db.users.find_one({"username": username})
        app_setup.mongo.db.recipes.update_one({"title" : recipe_title}, {"$inc": { "favourited": 1}})
        app_setup.mongo.db.users.update_one({"username": username}, {"$addToSet": {"favourite_recipes": recipe_title}})
        
    return redirect(url_for(page, recipe_title=recipe_title))
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)