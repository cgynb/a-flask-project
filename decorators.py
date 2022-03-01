from flask import g, redirect, url_for
from functools import wraps


def login_required(func):
    # @wraps(func) 如果不写，会使得函数改名改变，
    # url_for('user.login')这是login个函数，会变为wrapper
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
        if g.role == '商家':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('food.index'))
    return wrapper


def rider_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.role == '骑手':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('food.index'))
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.role == '管理员':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('food.index'))
    return wrapper
