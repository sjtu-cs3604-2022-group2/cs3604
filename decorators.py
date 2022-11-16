from flask import g, redirect, url_for, session

from functools import wraps


def login_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id"):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("user.login"))

    return wrapper
