import time
from flask_pymongo import PyMongo, pymongo
from app_setup import *

def get_top_ten_descending(field):
    return mongo.db.recipes.find().sort(field, pymongo.DESCENDING).limit(10)
    
def get_top_ten_ascending(field):
    return mongo.db.recipes.find().sort(field, pymongo.ASCENDING).limit(10)
    
def format_dates():
    recipes = get_top_ten_descending("creation_date")
    formatted_dates = []
    
    for recipe in recipes:
        formatted_dates.append(time.strftime("%d-%m-%Y", time.gmtime(recipe["creation_date"])))
    
    return formatted_dates