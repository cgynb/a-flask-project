from flask import g, redirect, url_for, flash
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))
    return wrapper


def merchant_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user.role == 2:
            return func(*args, **kwargs)
        else:
            flash('你没有注册为商家，不能进行此操作')
            return redirect(url_for('food.index'))
    return wrapper

