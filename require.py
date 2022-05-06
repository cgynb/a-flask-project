from flask import g, redirect, url_for, flash, session
from functools import wraps
# from data import create_token, verify_token


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            # token = verify_token(session.get('token'))
            # if token:
            #     if token.get('username') == g.user.username and token.get('user_id') == g.user.id:
            return func(*args, **kwargs)
        flash('登录吧hhh')
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


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user.role == 4:
            return func(*args, **kwargs)
        else:
            flash('你不是管理员，不能进行此操作')
            return redirect(url_for('food.index'))
    return wrapper
