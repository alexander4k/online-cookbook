import time
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId

from utils import app_setup, misc


def insert_user(username, password):
    """
    Creates a user object and inserts it into the database
    """
    
    user = {
        "username": username,
        "password": password,
        "favourite_recipes": []
    }
    
    app_setup.mongo.db.users.insert_one(user)
    
def create_recipe(title, description, image, author, servings, favourited, cuisine,
                category, difficulty, prep_time, cook_time, calories, fat, saturates,
                carbs, sugars, salt, fibre, protein, allergens, ingredients, instructions):
    """
    Creates a recipes object and returns it to be inserted into the database
    """
    
    recipe = {
            "title": title,
            "image": image,
            "author": author,
            "creation_date": time.time(),
            "description": description,
            "category": category,
            "cuisine": cuisine,
            "servings": servings,
            "favourited": favourited,
            "difficulty": difficulty,
            "time": {
                "cook": cook_time,
                "prep": prep_time
            },
            "allergens": allergens,
            "ingredients": ingredients,
            "instructions": instructions,
            "nutritional": {
                "calories": calories,
                "fat": fat,
                "saturates": saturates,
                "carbs": carbs,
                "sugars": sugars,
                "fibre": fibre,
                "protein": protein,
                "salt": salt
            }
        }
    
    return recipe
    
def get_top_ten_descending(field):
    """
    Returns ten items based on a given field from the database in descending order
    """
    return app_setup.mongo.db.recipes.find().sort(field, pymongo.DESCENDING).limit(10)
    
def get_top_ten_ascending(field):
    """
    Returns ten items based on a given field from the database in ascending order
    """
    return app_setup.mongo.db.recipes.find().sort(field, pymongo.ASCENDING).limit(10)
    
def format_dates(data):
    """
    Takes in a list of recipes returned from the database and converts
    their creation date(time in seconds since the epoch) to a string based on the format
    then adds the strings to a new list and returns it
    """
    recipes = data
    formatted_dates = []
        
    for recipe in recipes:
        formatted_dates.append(time.strftime("%d-%b-%Y", time.gmtime(recipe["creation_date"])))
        
    return formatted_dates

def format_date(data):
    """
    Takes in given time in seconds since the epoch and converts it 
    to a string based on the format and returns it
    """
    formatted_date = time.strftime("%d-%b-%Y", time.gmtime(data))
        
    return formatted_date
    
def assign_value(initial_value, value):
    """
    Used mainly when saving request data to a variable which
    is passed to a url. If value is equal to None returns given
    value.
    """
    field = initial_value
    if value != None:
        field = value
    return field

def set_filter_conditions(category_id, cuisine_id, ingredient, allergen, title):
    """
    Returns query conditions to be used when querying for recipes to return depending
    on what filter options where chosen/input by a user.
    """
    if category_id != None:
        condition_one = {"category": ObjectId(category_id)}
    else:
        condition_one = {}
    
    if cuisine_id != None:
        condition_two = {"cuisine": ObjectId(cuisine_id)}
    else:
        condition_two = {}

    if ingredient != "":
        # Searches for any documents which contain the given word/string in their ingredients, case insensitive
        condition_three = {"ingredients":{"$regex" : ".*" + ingredient + "*", "$options": 'si'}}
    else:
        condition_three = {}
    
    if allergen != None:
        # Searches for any documents which do not contain the given string/word in their allergens array
        condition_four = {"allergens": {"$nin": [allergen]}}
    else:
        condition_four = {}
        
    if title != "":
        # Searches for any documents with titles containing the given word/string, case insensitive
        condition_five = {"title":{"$regex" : ".*" + title + "*", "$options": 'si'}}
    else:
        condition_five = {}
    
    return (condition_one, condition_two, condition_three, condition_four, condition_five)
    
def set_sort_condition(sort):
    """
    Returns sort condition to be used when querying the database depending on what option a
    user has selected
    """
    if sort == "most_popular":
        sort_condition = ("favourited", pymongo.DESCENDING)
    elif sort == "least_popular":
        sort_condition = ("favourited", pymongo.ASCENDING)
    elif sort == "oldest": 
        sort_condition = ("creation_date", pymongo.ASCENDING)
    else:
        sort_condition = ("creation_date", pymongo.DESCENDING)
        
    return sort_condition
        
def filtered_recipes(category_id, cuisine_id, ingredient, allergen, title, to_skip, limit, sort):
    """
    Main function used for filtering recipes. Takes in users chosen filter and sort options and returns
    matching recipes. Allows for combining different filter options. Sets how many recipes are
    returned and how many skipped for pagination purposes. Also returns the number of found recipes.
    If no filters are set, returns all recipes.
    """
    conditions = set_filter_conditions(category_id, cuisine_id, ingredient, allergen, title)
    sort_condition = set_sort_condition(sort)

    if allergen != None or ingredient != "" or cuisine_id != None or category_id != None or title != "":
        filtered_recipes = app_setup.mongo.db.recipes.find(
            {"$and":
                [conditions[0], conditions[1], conditions[2], conditions[3], conditions[4]]
                
            }).skip(to_skip).limit(limit).sort(sort_condition[0], sort_condition[1])
        filtered_recipes_count = app_setup.mongo.db.recipes.find(
            {"$and": 
                [conditions[0], conditions[1], conditions[2], conditions[3], conditions[4]]
                
            }).count()
    else:
        filtered_recipes = app_setup.mongo.db.recipes.find().skip(to_skip).limit(limit).sort(sort_condition[0], sort_condition[1])
        filtered_recipes_count = app_setup.mongo.db.recipes.find().count()
        
    return (filtered_recipes, filtered_recipes_count)
    
def return_category_name(category_id):
    """
    Searches for a category document with a given id and returns the value of the name
    field
    """
    if category_id != None:
        category = app_setup.mongo.db.categories.find_one({"_id": ObjectId(category_id)})
        category_name = category["name"]
    else:
        category_name = ""
        
    return category_name
    
def return_cuisine_name(cuisine_id):
    """
    Searches for a cuisine document with a given id and returns the value of the name
    field
    """
    if cuisine_id != None:
        cuisine = app_setup.mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
        cuisine_name = cuisine["name"]
    else:
        cuisine_name = ""
        
    return cuisine_name
    
def return_allergen_name(allergen):
    """
    Returns the value if its not equal to None, else returns an empty string
    """
    if allergen != None:
        allergen_name = allergen
    else:
        allergen_name = ""
        
    return allergen_name
    