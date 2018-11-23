import os
import time
from flask import Flask, render_template, request, redirect, url_for, session
from bson.objectid import ObjectId
import validators

from utils import app_setup, queries, misc, sessions


app = app_setup.app

app.secret_key = os.urandom(16)
    
@app.route("/", defaults={"password_error": False, "username_error": False})
@app.route("/<password_error>/<username_error>/")
def index(password_error, username_error):
    username = None
    user = None

    if "user" in session:
        username = sessions.check_if_user_in_session()
        user = app_setup.mongo.db.users.find_one({"username": username})

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
                            user=user,
                            username_error=username_error,
                            password_error=password_error)

@app.route("/login", methods=["POST"])
def login():
    session.pop("user", None)
    password_error = False
    username_error = False
    
    if request.method == "POST":
        user = app_setup.mongo.db.users.find_one({"username": request.form.get("username")})
        if user != None:
            if request.form.get("password") == user["password"]:
                session["user"] = user["username"]
            else:
                password_error = True
        else:
            username_error = True

    return redirect(url_for("index", password_error=password_error, username_error=username_error))
                     
@app.route("/logout")
def logout():
    session.pop("user", None)
    
    return redirect(url_for("index"))

@app.route("/register_user/", defaults={"registration_error": False})
@app.route("/register_user/<registration_error>/")
def register_user(registration_error):
    session.pop("user", None)
    
    return render_template("register.html", registration_error=registration_error)
    
@app.route("/insert_user", methods=["POST"])
def insert_user():
    if app_setup.mongo.db.users.find({"username": request.form.get("username")}).count() == 0:
        queries.insert_user(request.form.get("username"),
                            request.form.get("password"))
        session["user"] = request.form.get("username")
        return redirect(url_for("index"))
    else:
        registration_error = True
        return redirect(url_for("register_user", registration_error=registration_error))
                            
@app.route("/account")
def account():
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    my_recipes_a = app_setup.mongo.db.recipes.find({"author": ObjectId(user["_id"])})
    my_recipes_b = app_setup.mongo.db.recipes.find({"author": ObjectId(user["_id"])})
    my_recipes_dates = queries.format_dates(my_recipes_b)
    all_recipes_a = app_setup.mongo.db.recipes.find()
    all_recipes_b = app_setup.mongo.db.recipes.find()
    all_recipes_dates = queries.format_dates(all_recipes_b)
    
    return render_template("account.html",
                            my_recipes_a=my_recipes_a,
                            user=user,
                            my_recipes_dates=my_recipes_dates,
                            all_recipes_dates=all_recipes_dates,
                            all_recipes_a=all_recipes_a)
    
@app.route("/add_recipe")
def add_recipe():
    username = sessions.check_if_user_in_session()
    cuisines = app_setup.mongo.db.cuisines.find()
    categories = app_setup.mongo.db.categories.find()
    
    return render_template("add_recipe.html",
                            categories=categories,
                            cuisines=cuisines,
                            username=username)
                            
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    cuisine = app_setup.mongo.db.cuisines.find_one({"name": request.form.get("cuisine")})
    category = app_setup.mongo.db.categories.find_one({"name": request.form.get("category")})

    if validators.url(request.form.get("image")) == True:
        image = request.form.get("image")
    else:
        image = "https://image.freepik.com/free-vector/different-kitchen-icons_1010-426.jpg"
            
    new_recipe = queries.create_recipe(request.form.get("title"),
                                    request.form.get("description"),
                                    image,
                                    user["_id"],
                                    request.form.get("servings"),
                                    0,
                                    cuisine["_id"],
                                    category["_id"],
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
    
@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    username = sessions.check_if_user_in_session()
    recipe = app_setup.mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cuisines = app_setup.mongo.db.cuisines.find()
    categories = app_setup.mongo.db.categories.find()
    current_category = app_setup.mongo.db.categories.find_one({"_id": recipe["category"]})
    current_cuisine = app_setup.mongo.db.cuisines.find_one({"_id": recipe["cuisine"]})
    
    difficulties = ["Easy", "Medium", "Hard"]
    
    return render_template("edit_recipe.html",
                            recipe=recipe,
                            categories=categories,
                            cuisines=cuisines,
                            current_category=current_category,
                            current_cuisine=current_cuisine,
                            difficulties=difficulties,
                            username=username)
                            
@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    if request.method == "POST":
        username = sessions.check_if_user_in_session()
        user = app_setup.mongo.db.users.find_one({"username": username})
        current_recipe = app_setup.mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        cuisine = app_setup.mongo.db.cuisines.find_one({"name": request.form.get("cuisine")})
        category = app_setup.mongo.db.categories.find_one({"name": request.form.get("category")})
        
        if validators.url(request.form.get("image")) == True:
            image = request.form.get("image")
        else:
            image = "https://image.freepik.com/free-vector/different-kitchen-icons_1010-426.jpg"
        
        new_recipe = queries.create_recipe(request.form.get("title"),
                                        request.form.get("description"),
                                        image,
                                        user["_id"],
                                        request.form.get("servings"),
                                        current_recipe["favourited"],
                                        cuisine["name"],
                                        category["name"],
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
                                        
        app_setup.mongo.db.recipes.replace_one({"_id": ObjectId(recipe_id)}, new_recipe)
    
    return redirect(url_for("recipe_details", recipe_id=recipe_id))
    
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    app_setup.mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    app_setup.mongo.db.users.update_many({}, { "$pull": { "favourite_recipes": ObjectId(recipe_id) } })
    
    return redirect(url_for("account"))
    
@app.route("/remove_recipe_favourite/<recipe_id>")
def remove_recipe_favourite(recipe_id):
    username = sessions.check_if_user_in_session()
    app_setup.mongo.db.users.update_one({"username": username}, { "$pull": { "favourite_recipes": ObjectId(recipe_id) } })
    app_setup.mongo.db.recipes.update_one({"_id" : ObjectId(recipe_id)}, {"$inc": { "favourited": -1}})
    
    return redirect(url_for("account"))
    
@app.route("/recipe_details/<recipe_id>")
def recipe_details(recipe_id):
    print(recipe_id)
    username = None
    user = None
    
    if "user" in session:
        username = sessions.check_if_user_in_session()
        user = app_setup.mongo.db.users.find_one({"username": username})
    
    recipe = app_setup.mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    author = app_setup.mongo.db.users.find_one({"_id": ObjectId(recipe["author"])})
    converted_creation_date = queries.format_date(recipe["creation_date"])
    cuisine = app_setup.mongo.db.cuisines.find_one({"_id": recipe["cuisine"]})
    time = recipe["time"]
    nutritional = recipe["nutritional"]
    nutrition_names = []
    nutrition_values = []
    
    for name, value in nutritional.items():
        nutrition_names.append(name)
        nutrition_values.append(value)
    
    return render_template("recipe_details.html",
                            recipe=recipe,
                            creation_date=converted_creation_date,
                            time=time,
                            nutrition_names=nutrition_names,
                            nutrition_values=nutrition_values,
                            username=username,
                            user=user,
                            author=author,
                            cuisine=cuisine)
                            
@app.route("/favourite/<recipe_id>/<page>")
def favourite(recipe_id, page):
    username = session["user"]
    user = app_setup.mongo.db.users.find_one({"username": username})
    
    app_setup.mongo.db.recipes.update_one({"_id" : ObjectId(recipe_id)}, {"$inc": { "favourited": 1}})
    app_setup.mongo.db.users.update_one({"username": username}, {"$addToSet": {"favourite_recipes": ObjectId(recipe_id)}})
        
    return redirect(url_for(page, recipe_id=recipe_id))
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)