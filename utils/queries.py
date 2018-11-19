import time
from flask_pymongo import PyMongo, pymongo
from utils import app_setup, misc

def get_top_ten_descending(field):
    return app_setup.mongo.db.recipes.find().sort(field, pymongo.DESCENDING).limit(10)
    
def get_top_ten_ascending(field):
    return app_setup.mongo.db.recipes.find().sort(field, pymongo.ASCENDING).limit(10)
    
def format_dates(data):
    recipes = data
    formatted_dates = []
        
    for recipe in recipes:
        formatted_dates.append(time.strftime("%d-%m-%Y", time.gmtime(recipe["creation_date"])))
        
    return formatted_dates

def format_date(data):
    formatted_date = time.strftime("%d-%m-%Y", time.gmtime(data))
        
    return formatted_date
    
def create_recipe(title,
                description,
                image,
                author,
                servings,
                favourited,
                cuisine,
                category,
                difficulty,
                prep_time,
                cook_time,
                calories,
                fat,
                saturates,
                carbs,
                sugars,
                salt,
                fibre,
                protein,
                allergens,
                ingredients,
                instructions):
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
    
    
    
    return(recipe)
    
def insert_user(username, password):
    user = {
        "username": username,
        "password": password,
        "my_recipes": [],
        "favourite_recipes": []
    }
    app_setup.mongo.db.users.insert_one(user)

def find_unique_items_in_list(list_of_items):
    list_lowercase = misc.convert_items_in_list_to_lower(list_of_items)
    list_set = set(list_lowercase)
    unique_items = list(list_set)
    return (unique_items)
    
def sort_list(list_to_sort):
    sorted_list = sorted(list_to_sort)
    return(sorted_list)
    
def return_capitalized_unique_items_in_list(list_to_search):
    unique_items = find_unique_items_in_list(list_to_search)
    sorted_list = sort_list(unique_items)
    capitalized = misc.convert_items_in_list_to_capitalized(sorted_list)
    return(capitalized)
    
def list_values(record):
    list_of_values = []
    for key, value in record.items():
        list_of_values.append(value)
        
    return(list_of_values)
    
    

