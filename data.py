import pprint
from models import UserModel
import time
import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


# def create_token(username, user_id):
#     s = Serializer(current_app.config['SECRET_KEY'], salt=current_app.config['SALT'])
#     token = s.dumps({"username": username, 'user_id': user_id}).decode("utf-8")
#     return token
#
#
# def verify_token(token):
#     s = Serializer(current_app.config['SECRET_KEY'], salt=current_app.config['SALT'])
#     try:
#         data = s.loads(token)
#     except BaseException as _:
#         print(_)
#         return None
#     return data


def turn_userid_to_name(userid):
    u = UserModel.query.filter(UserModel.id == userid).first()
    return u.username


def turn_username_to_id(username):
    u = UserModel.query.filter(UserModel.username == username).first()
    return u.id


def orderConbinition(order_list):
    info = []
    order_ids = {i['order_id'] for i in order_list}
    for order_id in order_ids:
        total_price = 0
        food = ''
        an_order = {'total_price': total_price, 'food': food, 'order_id': order_id}
        for order in order_list:
            if order['order_id'] == order_id:
                an_order['customer_id'] = order['customer_id']
                an_order['arrive'] = order['arrive']
                an_order['merchant_id'] = order['merchant_id']
                an_order['merchant_take_order'] = order['merchant_take_order']
                an_order['rider_id'] = order['rider_id']
                an_order['zan'] = order['zan']
                an_order['food'] += f"{order['food_name']}x{order['food_count']}"
                an_order['total_price'] += order['food_price'] * order['food_count']
                if order['rider_salary']:
                    an_order['rider_salary'] = order['rider_salary']
        # print(an_order)
        info.append(an_order)
    return info


if __name__ == '__main__':
    orders = [{'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 23, 'food_price': 30.0, 'food_name': '咖啡', 'food_count': 7,
               'zan': False, 'order_id': '21185685Bfbc843'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 24, 'food_price': 3.0, 'food_name': '土豆', 'food_count': 1, 'zan': False,
               'order_id': '21185685Bfbc843'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 23, 'food_price': 30.0, 'food_name': '咖啡', 'food_count': 2,
               'zan': False, 'order_id': '21186033MBxkD43'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 24, 'food_price': 3.0, 'food_name': '土豆', 'food_count': 7, 'zan': False,
               'order_id': '21186033MBxkD43'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 23, 'food_price': 30.0, 'food_name': '咖啡', 'food_count': 2,
               'zan': False, 'order_id': '211865679sEcNv3'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 24, 'food_price': 3.0, 'food_name': '土豆', 'food_count': 4, 'zan': False,
               'order_id': '211865679sEcNv3'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 23, 'food_price': 30.0, 'food_name': '咖啡', 'food_count': 1,
               'zan': False, 'order_id': '21193719jHc4lE3'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 23, 'food_price': 30.0, 'food_name': '咖啡', 'food_count': 2,
               'zan': False, 'order_id': '21220821CNaiZk3'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 24, 'food_price': 3.0, 'food_name': '土豆', 'food_count': 1, 'zan': False,
               'order_id': '21220821CNaiZk3'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 24, 'food_price': 3.0, 'food_name': '土豆', 'food_count': 1, 'zan': False,
               'order_id': '212216280YB3DI3'},
              {'customer_id': 3, 'arrive': False, 'merchant_id': 3, 'merchant_take_order': False, 'rider_id': None,
               'rider_salary': None, 'food_id': 23, 'food_price': 30.0, 'food_name': '咖啡', 'food_count': 1,
               'zan': False, 'order_id': '212216280YB3DI3'}]

    pprint.pprint(orderConbinition(orders))
