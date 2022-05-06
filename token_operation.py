# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 11:50
# @Author  : CGY
# @File    : token_operation.py
# @Project : NewWaiMai 
# @Comment : token
from flask import current_app
import jwt
from jwt import exceptions
import time


def create_token(user):
    headers = {
        "alg": "HS256",
        "typ": "JWT",
    }
    exp = int(time.time() + 3600)
    payload = {
        "name": user.username,
        "role": user.role,
        "user_id": user.id,
        "exp": exp,
        "iss": 'cgy'
    }
    token = jwt.encode(payload=payload, key=current_app.config.get('SECRET_KEY'), algorithm='HS256',
                       headers=headers)
    return token


def validate_token(token):
    payload = None
    msg = None
    try:
        payload = jwt.decode(jwt=token, key=current_app.config.get('SECRET_KEY'), algorithms=['HS256'], issuer='cgy')
    except exceptions.ExpiredSignatureError:
        msg = 'token已失效'
    except jwt.DecodeError:
        msg = 'token认证失败'
    except jwt.InvalidTokenError:
        msg = '非法的token'
    return payload, msg

