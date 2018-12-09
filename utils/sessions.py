from flask import session

def check_if_user_in_session():
    """
    Check if user is in session and if yes,
    return the user's username
    """
    username = None
    if "user" in session:
        username = session["user"]
    return username