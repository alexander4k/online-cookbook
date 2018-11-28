import time
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId

from utils import app_setup, misc


def get_top_ten_descending(field):
    return app_setup.mongo.db.recipes.find().sort(field, pymongo.DESCENDING).limit(10)
    
def get_top_ten_ascending(field):
    return app_setup.mongo.db.recipes.find().sort(field, pymongo.ASCENDING).limit(10)
    
def format_dates(data):
    recipes = data
    formatted_dates = []
        
    for recipe in recipes:
        formatted_dates.append(time.strftime("%d-%m-%Y-%H-%M-%S", time.gmtime(recipe["creation_date"])))
        
    return formatted_dates

def format_date(data):
    formatted_date = time.strftime("%d-%m-%Y", time.gmtime(data))
        
    return formatted_date
    
def create_recipe(title, description, image, author, servings, favourited, cuisine,
                category, difficulty, prep_time, cook_time, calories, fat, saturates,
                carbs, sugars, salt, fibre, protein, allergens, ingredients, instructions):
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
    
def insert_user(username, password):
    user = {
        "username": username,
        "password": password,
        "favourite_recipes": []
    }
    
    app_setup.mongo.db.users.insert_one(user)

def find_unique_items_in_list(list_of_items):
    list_lowercase = misc.convert_items_in_list_to_lower(list_of_items)
    list_set = set(list_lowercase)
    unique_items = list(list_set)
    
    return unique_items
    
def sort_list(list_to_sort):
    sorted_list = sorted(list_to_sort)
    
    return sorted_list
    
def return_capitalized_unique_items_in_list(list_to_search):
    unique_items = find_unique_items_in_list(list_to_search)
    sorted_list = sort_list(unique_items)
    capitalized = misc.convert_items_in_list_to_capitalized(sorted_list)
    
    return capitalized
    
def list_values(record):
    list_of_values = []
    for key, value in record.items():
        list_of_values.append(value)
        
    return list_of_values
    
def set_filter_title(title_filter):
    title = None
    
    if title_filter != None:
        title = title_filter 
    
    return title

def set_filter_ingredient(ingredient_filter):
    ingredient = None
    
    if ingredient_filter != None:
        ingredient = ingredient_filter
        
    return ingredient
    
def set_filter_allergen(allergen_filter):
    allergen = None
    
    if allergen_filter != None:
        allergen = allergen_filter
        
    return allergen
    
def set_filter_category(category_filter):
    category_id = None
    
    if category_filter != None:
        category = app_setup.mongo.db.categories.find_one({"name": category_filter})
        category_id = category["_id"]
        
    return category_id
    
def set_filter_cuisine(cuisine_filter):
    cuisine_id = None
    
    if cuisine_filter != None:
        cuisine = app_setup.mongo.db.cuisines.find_one({"name": cuisine_filter})
        cuisine_id = cuisine["_id"]
        
    return cuisine_id

def assign_value(initial_value, value):
    field = initial_value
    if value != None:
        field = value
    return field

        
def set_filter_conditions(category_id, cuisine_id, ingredient, allergen, title):
    if category_id != None:
        condition_one = {"category": ObjectId(category_id)}
    else:
        condition_one = {}
    
    if cuisine_id != None:
        condition_two = {"cuisine": ObjectId(cuisine_id)}
    else:
        condition_two = {}

    if ingredient != "":
        condition_three = {"ingredients":{"$regex" : ".*" + ingredient + "*", "$options": 'si'}}
    else:
        condition_three = {}
    
    if allergen != None:
        condition_four = {"allergens": {"$nin": [allergen]}}
    else:
        condition_four = {}
        
    if title != "":
        condition_five = {"title":{"$regex" : ".*" + title + "*", "$options": 'si'}}
    else:
        condition_five = {}
    
    return (condition_one, condition_two, condition_three, condition_four, condition_five)
    
def set_sort_condition(sort):
    if sort == "most_popular":
        sort_condition = ("favourited", pymongo.DESCENDING)
        print(sort_condition)
    elif sort == "least_popular":
        sort_condition = ("favourited", pymongo.ASCENDING)
    elif sort == "oldest": 
        sort_condition = ("creation_date", pymongo.ASCENDING)
    else:
        sort_condition = ("creation_date", pymongo.DESCENDING)
        
    return sort_condition
        
def filtered_recipes(category_id, cuisine_id, ingredient, allergen, title, to_skip, limit, sort):
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
    if category_id != None:
        category = app_setup.mongo.db.categories.find_one({"_id": ObjectId(category_id)})
        category_name = category["name"]
    else:
        category_name = ""
        
    return category_name
    
def return_cuisine_name(cuisine_id):
    if cuisine_id != None:
        cuisine = app_setup.mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
        cuisine_name = cuisine["name"]
    else:
        cuisine_name = ""
        
    return cuisine_name
    
def return_allergen_name(allergen):
    if allergen != None:
        allergen_name = allergen
    else:
        allergen_name = ""
        
    return allergen_name
    