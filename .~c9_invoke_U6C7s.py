import os
import time
from flask import Flask, render_template, request, redirect, url_for, session
from bson.objectid import ObjectId
from flask_pymongo import PyMongo, pymongo
import validators

from utils import app_setup, queries, misc, sessions


app = app_setup.app

@app.route("/", defaults={"password_error": False, "username_error": False})
@app.route("/<password_error>/<username_error>/")
def index(password_error, username_error):
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    
    """
    Get recipes for display on the carousels
    """
    most_popular = queries.get_top_ten_descending("favourited")
    recent = queries.get_top_ten_descending("creation_date")
    oldest = queries.get_top_ten_ascending("creation_date")
    popular_dates = queries.format_dates(queries.get_top_ten_descending("favourited"))
    recent_dates = queries.format_dates(queries.get_top_ten_descending("creation_date"))
    oldest_dates = queries.format_dates(queries.get_top_ten_ascending("creation_date"))
    
    """
    Find documents for displaying the summary nav section
    """
    categories = app_setup.mongo.db.categories.find()
    categories_two = app_setup.mongo.db.categories.find()
    cuisines = app_setup.mongo.db.cuisines.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]
    
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
                            password_error=password_error,
                            categories=categories,
                            categories_two=categories_two,
                            cuisines=cuisines,
                            cuisines_two=cuisines_two,
                            allergens=allergens)
                            
@app.route("/summary_display", methods=["GET", "POST"])
def summary_display():
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    
    """
    Find documents for displaying the summary nav section
    """
    categories = app_setup.mongo.db.categories.find()
    categories_two = app_setup.mongo.db.categories.find()
    cuisines = app_setup.mongo.db.cuisines.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]
    
    recipes = []
    recipes_dates = []
    recipes_count = 0
    category = None
    cuisine = None
    allergen = None
    
    page_number = 1
    
    """
    Assign page number based on which pagination link a user activated
    """
    if request.args.get("page_number") != None:
        page_number = queries.assign_value(1, int(request.args.get("page_number")))
        
    sort = "newest"
    
    """
    Assign sort based on which option a user selected to sort recipes on page
    """
    if request.method == "POST":
        if request.form.get("sort"):
            sort = queries.assign_value("newest", request.form.get("sort"))
        else:
            sort = "newest"
    
    """
    Set the number of recipes to skip according to page number, 
    set the sort condition to be used while querying and get the total number
    of recipes in the database to compare against
    """
    to_skip = misc.set_number_to_skip(9, page_number) 
    sort_condition = queries.set_sort_condition(sort)
    all_recipes_count = app_setup.mongo.db.recipes.find().count()
    
    """
    Recipes to return depending on which option a user selects in the summary nav section.
    Also gets a formatted list of dates for these recipes, the number of recipes returned and
    the name of the option a user has selected.
    """
    if request.args.get("selected_category") != None and request.args.get("selected_category") != "":
        recipes = app_setup.mongo.db.recipes.find(
            {"category": ObjectId(request.args.get("selected_category"))}).skip(to_skip).limit(9).sort(sort_condition[0], sort_condition[1])
        recipes_dates = queries.format_dates(app_setup.mongo.db.recipes.find(
            {"category": ObjectId(request.args.get("selected_category"))}).sort(sort_condition[0], sort_condition[1]))
        recipes_count = app_setup.mongo.db.recipes.find(
            {"category": ObjectId(request.args.get("selected_category"))}).count()
        category = app_setup.mongo.db.categories.find_one(
            {"_id": ObjectId(request.args.get("selected_category"))})
        
    elif request.args.get("selected_cuisine") != None and request.args.get("selected_cuisine") != "":
        recipes = app_setup.mongo.db.recipes.find(
            {"cuisine": ObjectId(request.args.get("selected_cuisine"))}).skip(to_skip).limit(9).sort(sort_condition[0], sort_condition[1])
        recipes_dates = queries.format_dates(app_setup.mongo.db.recipes.find(
            {"cuisine": ObjectId(request.args.get("selected_cuisine"))}).sort(sort_condition[0], sort_condition[1]))
        recipes_count = app_setup.mongo.db.recipes.find(
            {"cuisine": ObjectId(request.args.get("selected_cuisine"))}).count()
        cuisine = app_setup.mongo.db.cuisines.find_one(
            {"_id": ObjectId(request.args.get("selected_cuisine"))})
        
    elif request.args.get("selected_allergen") != None and request.args.get("selected_allergen") != "":
        recipes = app_setup.mongo.db.recipes.find(
            {"allergens": {"$nin": [request.args.get("selected_allergen")]}}).skip(to_skip).limit(9).sort(sort_condition[0], sort_condition[1])
        recipes_dates = queries.format_dates(app_setup.mongo.db.recipes.find(
            {"allergens": {"$nin": [request.args.get("selected_allergen")]}}).sort(sort_condition[0], sort_condition[1]))
        recipes_count = app_setup.mongo.db.recipes.find(
            {"allergens": {"$nin": [request.args.get("selected_allergen")]}}).count()
        allergen = request.args.get("selected_allergen")
        
    """
    Gets the number of links to appear on the page and sets the prev_page and next_page
    behaviour
    """
    number_of_links = misc.calculate_number_of_pagination_links(9, recipes_count)
    prev_page = misc.set_prev_and_next_page_number(page_number, number_of_links)[0]
    next_page = misc.set_prev_and_next_page_number(page_number, number_of_links)[1]   
    
    return render_template("summary_display.html",
                            username=username,
                            user=user,
                            category=category,
                            cuisine=cuisine,
                            allergen=allergen,
                            recipes=recipes,
                            recipes_dates=recipes_dates,
                            recipes_count=recipes_count,
                            all_recipes_count=all_recipes_count,
                            page_number=page_number,
                            number_of_links=number_of_links,
                            prev_page=prev_page,
                            next_page=next_page,
                            sort=sort,
                            categories=categories,
                            categories_two=categories_two,
                            cuisines=cuisines,
                            cuisines_two=cuisines_two,
                            allergens=allergens,
                            cat=categories)

@app.route("/login", methods=["POST"])
def login():
    """
    In case a user is logged in, remove them from the session then add them once
    they input a username and password that matches one of the user documents in the 
    database. 
    """
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

    return redirect(url_for("index",
                            password_error=password_error,
                            username_error=username_error))
                     
@app.route("/logout")
def logout():
    """
    Remove a user from the session to log them out
    """
    session.pop("user", None)
    
    return redirect(url_for("index"))

@app.route("/register_user/", defaults={"registration_error": False})
@app.route("/register_user/<registration_error>/")
def register_user(registration_error):
    """
    If a user is in session, remove them before letting them register
    """
    session.pop("user", None)
    
    """
    Find documents for displaying the summary nav section
    """
    categories = app_setup.mongo.db.categories.find()
    categories_two = app_setup.mongo.db.categories.find()
    cuisines = app_setup.mongo.db.cuisines.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]
    
    return render_template("register.html",
                            registration_error=registration_error,
                            categories=categories,
                            categories_two=categories_two,
                            cuisines=cuisines,
                            cuisines_two=cuisines_two,
                            allergens=allergens)
    
@app.route("/insert_user", methods=["POST"])
def insert_user():
    """
    If a user tries to create an account with an existing username, return an error,
    otherwise create a user object, insert them into the databse and add the new user
    to session
    """
    if app_setup.mongo.db.users.find({"username": request.form.get("username")}).count() == 0:
        queries.insert_user(request.form.get("username"),
                            request.form.get("password"))
        session["user"] = request.form.get("username")
        
        return redirect(url_for("index"))
    else:
        registration_error = True
        
        return redirect(url_for("register_user",
                                registration_error=registration_error))
                            
@app.route("/account", methods=["GET", "POST"])
def account():
    """
    In case a user isn't logged in bring them back to the homepage
    """
    if "user" not in session:
        return redirect(url_for("index"))
        
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    sort = "newest"
    
    if request.method == "POST":
        if request.form.get("sort"):
            sort = queries.assign_value("newest", request.form.get("sort"))
        else:
            sort = "newest"
        
        """
        Redirect a user to the favourite_recipes page if they select option 2
        """
        if request.form.get("options"):
            if request.form.get("options") == "1":
                
                return redirect(url_for("account"))
            else:
                return redirect(url_for("favourite_recipes"))
        
    page_number = 1
    
    if request.args.get("page_number") != None:
        page_number = queries.assign_value(1, int(request.args.get("page_number")))
        
    to_skip = misc.set_number_to_skip(9, page_number) 
    sort_condition = queries.set_sort_condition(sort)
    
    """
    Find and return all the recipes created by the user
    """
    recipes = app_setup.mongo.db.recipes.find(
        {"author": ObjectId(user["_id"])}).skip(to_skip).limit(9).sort(sort_condition[0], sort_condition[1])
        
    recipes_dates = queries.format_dates(app_setup.mongo.db.recipes.find(
        {"author": ObjectId(user["_id"])}).sort(sort_condition[0], sort_condition[1]))
    recipes_count = app_setup.mongo.db.recipes.find({"author": ObjectId(user["_id"])}).count()
    
    number_of_links = misc.calculate_number_of_pagination_links(9, recipes_count)
    prev_page = misc.set_prev_and_next_page_number(page_number, number_of_links)[0]
    next_page = misc.set_prev_and_next_page_number(page_number, number_of_links)[1]   
    
    """
    Find documents for displaying the summary nav section
    """
    categories = app_setup.mongo.db.categories.find()
    categories_two = app_setup.mongo.db.categories.find()
    cuisines = app_setup.mongo.db.cuisines.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]
    
    return render_template("account.html",
                            recipes=recipes,
                            user=user,
                            recipes_count=recipes_count,
                            recipes_dates=recipes_dates,
                            page_number=page_number,
                            nex_page=next_page,
                            prev_page=prev_page,
                            number_of_links=number_of_links,
                            sort=sort,
                            categories=categories,
                            categories_two=categories_two,
                            cuisines=cuisines,
                            cuisines_two=cuisines_two,
                            allergens=allergens)
                            
@app.route("/favourite_recipes", methods=["GET", "POST"])
def favourite_recipes():
    """
    In case a user isn't logged in bring them back to the homepage
    """
    if "user" not in session:
        return redirect(url_for("index"))
        
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    
    sort = "newest"
    
    if request.method == "POST":
        if request.form.get("sort"):
            sort = queries.assign_value("newest", request.form.get("sort"))
        else:
            sort = "newest"
            
        if request.form.get("options"):
            if request.form.get("options") == "1":
                return redirect(url_for("account"))
            else:
                return redirect(url_for("favourite_recipes"))
        
    page_number = 1
    
    if request.args.get("page_number") != None:
        page_number = queries.assign_value(1, int(request.args.get("page_number")))
    
    to_skip = misc.set_number_to_skip(9, page_number)     
    limit = to_skip + 9
    sort_condition = queries.set_sort_condition(sort)
    
    """
    Get all recipes then compare their ids with a users favourite recipes list which contains 
    recipe ids. Those that match add to a new list and add their creation dates to another list.
    
    """
    recipes = app_setup.mongo.db.recipes.find().sort(sort_condition[0], sort_condition[1])
    recipes_dates = queries.format_dates(app_setup.mongo.db.recipes.find().sort(sort_condition[0], sort_condition[1]))
    
    favourite_recipes = []
    favourite_recipes_dates = []
    
    for index, recipe in enumerate(recipes):
        if recipe["_id"] in user["favourite_recipes"]:
            favourite_recipes.append(recipe)
            favourite_recipes_dates.append(recipes_dates[index])
    
    """
    Get the number of favourite recipes and get recipes with index numbers
    between to_skip and limit for displaying on the page 
    """
    favourite_recipes_count = len(favourite_recipes)
    favourite_recipes_skip_limit = favourite_recipes[to_skip:limit]

    number_of_links = misc.calculate_number_of_pagination_links(9, favourite_recipes_count)
    prev_page = misc.set_prev_and_next_page_number(page_number, number_of_links)[0]
    next_page = misc.set_prev_and_next_page_number(page_number, number_of_links)[1]
    
    """
    Find documents for displaying the summary nav section
    """
    categories = app_setup.mongo.db.categories.find()
    categories_two = app_setup.mongo.db.categories.find()
    cuisines = app_setup.mongo.db.cuisines.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]
    
    return render_template("favourites.html",
                            recipes=favourite_recipes_skip_limit,
                            favourite_recipes_count=favourite_recipes_count,
                            user=user,
                            recipes_dates=favourite_recipes_dates,
                            page_number=page_number,
                            nex_page=next_page,
                            prev_page=prev_page,
                            number_of_links=number_of_links,
                            sort=sort,
                            categories=categories,
                            categories_two=categories_two,
                            cuisines=cuisines,
                            cuisines_two=cuisines_two,
                            allergens=allergens)
    
@app.route("/add_recipe")
def add_recipe():
    """
    In case a user isn't logged in bring them back to the homepage
    """
    if "user" not in session:
        return redirect(url_for("index"))
        
    username = sessions.check_if_user_in_session()
    cuisines = app_setup.mongo.db.cuisines.find()
    categories = app_setup.mongo.db.categories.find()
    
    """
    Find documents for displaying the summary nav section
    """
    categories_two = app_setup.mongo.db.categories.find()
    categories_three = app_setup.mongo.db.categories.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    cuisines_three = app_setup.mongo.db.cuisines.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]
    
    return render_template("add_recipe.html",
                            categories=categories,
                            cuisines=cuisines,
                            username=username,
                            categories_two=categories_two,
                            categories_three=categories_three,
                            cuisines_two=cuisines_two,
                            cuisines_three=cuisines_three,
                            allergens=allergens)
                            
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    """
    In case a user isn't logged in bring them back to the homepage
    """
    if "user" not in session:
        return redirect(url_for("index"))
        
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    
    """
    Find a cuisine and category document based on user input 
    """
    cuisine = app_setup.mongo.db.cuisines.find_one({"name": request.form.get("cuisine")})
    category = app_setup.mongo.db.categories.find_one({"name": request.form.get("category")})
    
    """
    Check if the url a user inputs is a valid url, if not, assign a default image url in order to
    avoid having recipes with no image
    """
    if validators.url(request.form.get("image")) == True:
        image = request.form.get("image")
    else:
        image = "https://image.freepik.com/free-vector/different-kitchen-icons_1010-426.jpg"
    
    """
    Create a new recipe object and insert it into the database. Set the author of the recipe
    as the user documents id for reference, and the same for cuisine and category fields.
    Set the number of times the recipe has been favourited as 0.
    If a user submits the form containing blank ingredient or instruction fields, filter them out.
    Covert the resulting filter object back to a list.
    """
    new_recipe = queries.create_recipe(request.form.get("title"),
                                    request.form.get("description"),
                                    image,
                                    user["_id"],
                                    request.form.get("servings"),
                                    0,
                                    ObjectId(cuisine["_id"]),
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
                                    list(filter(None, request.form.getlist("ingredient"))),
                                    list(filter(None, request.form.getlist("instruction"))))

    app_setup.mongo.db.recipes.insert_one(new_recipe)
                           
    return redirect(url_for("account")) 
    
@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    """
    In case a user isn't logged in bring them back to the homepage
    """
    if "user" not in session:
        return redirect(url_for("index"))
        
    username = sessions.check_if_user_in_session()
    recipe = app_setup.mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cuisines = app_setup.mongo.db.cuisines.find()
    categories = app_setup.mongo.db.categories.find()
    current_category = app_setup.mongo.db.categories.find_one({"_id": recipe["category"]})
    current_cuisine = app_setup.mongo.db.cuisines.find_one({"_id": recipe["cuisine"]})
    difficulties = ["Easy", "Medium", "Hard"]
    
    """
    Find documents for displaying the summary nav section
    """
    categories_two = app_setup.mongo.db.categories.find()
    categories_three = app_setup.mongo.db.categories.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    cuisines_three = app_setup.mongo.db.cuisines.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]
    
    return render_template("edit_recipe.html",
                            recipe=recipe,
                            categories=categories,
                            cuisines=cuisines,
                            current_category=current_category,
                            current_cuisine=current_cuisine,
                            difficulties=difficulties,
                            username=username,
                            categories_two=categories_two,
                            categories_three=categories_three,
                            cuisines_two=cuisines_two,
                            cuisines_three=cuisines_three,
                            allergens=allergens)
                            
@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    """
    In case a user isn't logged in bring them back to the homepage
    """
    if "user" not in session:
        return redirect(url_for("index"))
        
    """
    Update a given recipe document in the database with new data
    """
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
                                        list(filter(None, request.form.getlist("ingredient"))),
                                        list(filter(None, request.form.getlist("instruction"))))
                                        
        app_setup.mongo.db.recipes.replace_one({"_id": ObjectId(recipe_id)}, new_recipe)
    
    return redirect(url_for("recipe_details",
                            recipe_id=recipe_id))
    
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """
    In case a user isn't logged in bring them back to the homepage
    """
    if "user" not in session:
        return redirect(url_for("index"))
        
    """
    Delete a matching recipe document from the database and that documents id
    from all the user documents favourite_recipes field so as to avoid referencing
    documents which no longer exist in the database
    """
    app_setup.mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    app_setup.mongo.db.users.update_many(
        {}, { "$pull": { "favourite_recipes": ObjectId(recipe_id) } })
    
    return redirect(url_for("account"))
    
@app.route("/remove_recipe_favourite/<recipe_id>")
def remove_recipe_favourite(recipe_id):
    """
    In case a user isn't logged in bring them back to the homepage
    """
    if "user" not in session:
        return redirect(url_for("index"))
        
    username = sessions.check_if_user_in_session()
    """
    Remove a given recipe id just from the user's favourite_recipes field and decrement
    that recipe's favourited field by 1 to reflect that it has been unfavourited
    """
    app_setup.mongo.db.users.update_one(
        {"username": username},{ "$pull": { "favourite_recipes": ObjectId(recipe_id) } })
    app_setup.mongo.db.recipes.update_one({"_id" : ObjectId(recipe_id)}, {"$inc": { "favourited": -1}})
    
    return redirect(url_for("favourite_recipes"))
    
@app.route("/recipe_details/<recipe_id>")
def recipe_details(recipe_id):
    """
    Find a given recipe document and get its details
    """
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
        
    """
    Find documents for displaying the summary nav section
    """
    categories = app_setup.mongo.db.categories.find()
    categories_two = app_setup.mongo.db.categories.find()
    cuisines = app_setup.mongo.db.cuisines.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]
    
    
    return render_template("recipe_details.html",
                            recipe=recipe,
                            creation_date=converted_creation_date,
                            time=time,
                            nutrition_names=nutrition_names,
                            nutrition_values=nutrition_values,
                            username=username,
                            user=user,
                            author=author,
                            cuisine=cuisine,
                            categories=categories,
                            categories_two=categories_two,
                            cuisines=cuisines,
                            cuisines_two=cuisines_two,
                            allergens=allergens)

@app.route("/all_recipes/", methods=["GET", "POST"])
def all_recipes():
    username = sessions.check_if_user_in_session()
    user = app_setup.mongo.db.users.find_one({"username": username})
    all_recipes_count = app_setup.mongo.db.recipes.find().count()
    cuisines = app_setup.mongo.db.cuisines.find()
    categories = app_setup.mongo.db.categories.find()
    allergens = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]

    if request.method == "POST":
        sort = queries.assign_value("newest", request.form.get("sort"))
    else:
        sort = "newest"
    
    """
    Save the current filter options so as not to reset them when paginating or sorting
    the filtered recipes on the page
    """
    title = queries.assign_value("", request.args.get("title_input"))
    ingredient = queries.assign_value("", request.args.get("ingredient_input"))
    allergen = request.args.get("allergen_input")
    allergen_name = queries.return_allergen_name(request.args.get("allergen_input"))
    cuisine_id = request.args.get("cuisine_input")
    cuisine_name = queries.return_cuisine_name(request.args.get("cuisine_input"))
    category_id = request.args.get("category_input")
    category_name = queries.return_category_name(request.args.get("category_input"))
    
    page_number = 1
    if request.args.get("page_number") != None:
        page_number = queries.assign_value(1, int(request.args.get("page_number")))
    
    to_skip = misc.set_number_to_skip(9, page_number)    
    
    recipes_dates = queries.format_dates(
        queries.filtered_recipes(category_id, cuisine_id, ingredient, allergen, title, to_skip, 9, sort)[0])
    recipes = queries.filtered_recipes(category_id, cuisine_id, ingredient, allergen, title, to_skip, 9, sort)[0]
    recipes_count = queries.filtered_recipes(category_id, cuisine_id, ingredient, allergen, title, 0, 9, sort)[1]
    
    number_of_pagination_links = misc.calculate_number_of_pagination_links(9, recipes_count)
    prev_page = misc.set_prev_and_next_page_number(page_number, number_of_pagination_links)[0]
    next_page = misc.set_prev_and_next_page_number(page_number, number_of_pagination_links)[1]
    
    """
    Find documents for displaying the summary nav section
    """
    categories_two = app_setup.mongo.db.categories.find()
    categories_three = app_setup.mongo.db.categories.find()
    cuisines_two = app_setup.mongo.db.cuisines.find()
    cuisines_three = app_setup.mongo.db.cuisines.find()
    allergens_two = ["dairy", "wheat", "eggs", "fish", "soy", "peanuts", "shellfish", "tree nuts"]

    return render_template("all_recipes.html",
                            user=user,
                            username=username,
                            recipes=recipes,
                            recipes_dates=recipes_dates,
                            cuisines=cuisines,
                            categories=categories,
                            allergens=allergens,
                            all_recipes_count=all_recipes_count,
                            recipes_count=recipes_count,
                            title=title,
                            ingredient=ingredient,
                            allergen=allergen,
                            allergen_name=allergen_name,
                            category_id=category_id,
                            category_name=category_name,
                            cuisine_id=cuisine_id,
                            cuisine_name=cuisine_name,
                            sort=sort,
                            prev_page=prev_page,
                            next_page=next_page,
                            number_of_pagination_links=number_of_pagination_links,
                            page_number=page_number,
                            categories_two=categories_two,
                            categories_three=categories_three,
                            cuisines_two=cuisines_two,
                            cuisines_three=cuisines_three,
                            allergens_two=allergens_two)
                            
@app.route("/filter_recipes", methods=["GET"])
def filter_recipes():
    """
    Save filter options selected by user to variables and pass them back to the all_recipes
    page
    """
    category = queries.assign_value(None, app_setup.mongo.db.categories.find_one({"name": request.args.get("category")}))
    cuisine = queries.assign_value(None, app_setup.mongo.db.cuisines.find_one({"name": request.args.get("cuisine")}))
    
    title_input = queries.assign_value(None, request.args.get("title"))
    ingredient_input = queries.assign_value(None, request.args.get("ingredient"))
    allergen_input = queries.assign_value(None, request.args.get("allergen"))
    
    if category != None:
        category_input = queries.assign_value(None, category["_id"])
    else:
        category_input = None
        
    if cuisine != None:
        cuisine_input = queries.assign_value(None, cuisine["_id"])
    else:
        cuisine_input = None
    
    return redirect(url_for("all_recipes", 
                            category_input=category_input,
                            cuisine_input=cuisine_input,
                            ingredient_input=ingredient_input,
                            allergen_input=allergen_input,
                            title_input=title_input))
                            
                            
@app.route("/favourite/<recipe_id>/<page>")
def favourite(recipe_id, page):
    username = session["user"]
    user = app_setup.mongo.db.users.find_one({"username": username})
    
    """
    Increment the value of favourited field for a given recipe by one to reflect that it has
    been favourited and add the id of that recipe to the user's favourite_recipes field for reference
    """
    app_setup.mongo.db.recipes.update_one({"_id" : ObjectId(recipe_id)}, {"$inc": { "favourited": 1}})
    app_setup.mongo.db.users.update_one(
        {"username": username},{"$addToSet": {"favourite_recipes": ObjectId(recipe_id)}})
        
    return redirect(url_for(page, recipe_id=recipe_id))

    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)