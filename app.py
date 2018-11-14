import os
import time
from flask import Flask, render_template

from utils import setup, queries 


app = setup.app

@app.route("/")
def home():
    
    
    recent = queries.get_top_ten_descending("creation_date")
    most_popular = queries.get_top_ten_descending("votes")
    least_popular = queries.get_top_ten_ascending("votes")
    
    formatted_dates = queries.format_dates()
    return render_template("home.html", most_popular=most_popular, recent=recent, least_popular=least_popular, formatted_dates=formatted_dates)
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)