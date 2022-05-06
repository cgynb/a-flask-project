# -*- coding: utf-8 -*-
# @Time    : 2022/4/28 17:35
# @Author  : CGY
# @File    : funcs.py
# @Project : NewWaiMai 
# @Comment : funcs
import yaml


CASES_PATH = 'cases/'
VIEW_CASES_PATH = 'view_cases/'
API_CASES_PATH = 'api_cases/'


def login_cases():
    with open(CASES_PATH + VIEW_CASES_PATH + 'login_case.yaml', 'r', encoding='utf-8') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def change_username_cases():
    with open(CASES_PATH + VIEW_CASES_PATH + 'change_username_case.yaml', 'r', encoding='utf-8') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def chatroom_cases():
    with open(CASES_PATH + VIEW_CASES_PATH + 'chatroom_case.yaml', 'r', encoding='utf-8') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- TAG ---------
def post_tag_cases():
    with open(CASES_PATH + API_CASES_PATH + 'tag_cases/post.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def delete_tag_cases():
    with open(CASES_PATH + API_CASES_PATH + 'tag_cases/delete.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- NOTICE ---------
def post_notice_cases():
    with open(CASES_PATH + API_CASES_PATH + 'notice_cases/post.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- ZAN ---------
def put_zan_cases():
    with open(CASES_PATH + API_CASES_PATH + 'zan_cases/put.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- MSG ---------
def get_room_msg_cases():
    with open(CASES_PATH + API_CASES_PATH + 'message_cases/get_room.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def get_self_msg_cases():
    with open(CASES_PATH + API_CASES_PATH + 'message_cases/get_self.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- FOLLOW ---------
def get_follow_list_cases():
    with open(CASES_PATH + API_CASES_PATH + 'follow_cases/get_follow_list.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def get_if_follow_cases():
    with open(CASES_PATH + API_CASES_PATH + 'follow_cases/get_if_follow.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def get_merchant_follow_cases():
    with open(CASES_PATH + API_CASES_PATH + 'follow_cases/get_merchant_follow.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def post_follow_cases():
    with open(CASES_PATH + API_CASES_PATH + 'follow_cases/post.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def delete_follow_cases():
    with open(CASES_PATH + API_CASES_PATH + 'comment_cases/delete.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- COMMENT ---------
def get_comment_cases():
    with open(CASES_PATH + API_CASES_PATH + 'comment_cases/get.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def post_comment_cases():
    with open(CASES_PATH + API_CASES_PATH + 'comment_cases/post.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def put_comment_cases():
    with open(CASES_PATH + API_CASES_PATH + 'comment_cases/put.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def delete_comment_cases():
    with open(CASES_PATH + API_CASES_PATH + 'comment_cases/delete.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- FOOD ---------
def get_food_cases():
    with open(CASES_PATH + API_CASES_PATH + 'food_cases/get.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def post_food_cases():
    with open(CASES_PATH + API_CASES_PATH + 'food_cases/post.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def put_food_cases():
    with open(CASES_PATH + API_CASES_PATH + 'food_cases/put.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def delete_food_cases():
    with open(CASES_PATH + API_CASES_PATH + 'food_cases/delete.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- USER ---------
def get_user_cases():
    with open(CASES_PATH + API_CASES_PATH + 'userinfo_cases/get.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def put_user_cases():
    with open(CASES_PATH + API_CASES_PATH + 'userinfo_cases/put.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def delete_user_cases():
    with open(CASES_PATH + API_CASES_PATH + 'userinfo_cases/delete.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


# --------- ORDER ---------
def get_order_cases():
    with open(CASES_PATH + API_CASES_PATH + 'order_cases/get.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases


def put_order_cases():
    with open(CASES_PATH + API_CASES_PATH + 'order_cases/put.yaml') as f:
        cases = yaml.load(f, yaml.FullLoader)
    return cases

