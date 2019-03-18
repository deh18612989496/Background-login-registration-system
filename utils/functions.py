from functools import wraps

from flask import session, url_for, redirect


def is_login(func):
    @wraps(func)
    def check():
        user_id = session.get('user_id')
        if user_id:
            return func()
        else:
            return redirect(url_for('back.login'))
        return func
    return check