from flask import session

def check_if_user_in_session():
    username = None
    if "user" in session:
        username = session["user"]
    return username