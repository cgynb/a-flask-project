# -*- coding: utf-8 -*-
# @Time    : 2022/4/29 0:46
# @Author  : CGY
# @File    : test_api.py
# @Project : NewWaiMai 
# @Comment : api test
import pytest
from jsonschema import validate
from schemas import *
from funcs import *
from app import app


@pytest.mark.usefixtures('customer_client')
class Test_TagApi:
    def test_get(self, customer_client):
        resp = customer_client.get('/elebu/api/v1/tag/')
        validate(instance=resp.json, schema=GET_TAG_SCHEMA)
        assert resp['status'] == 200

    @pytest.mark.parametrize('cases', post_tag_cases())
    def test_post(self, customer_client, cases):
        resp = customer_client.post('/elebu/api/v1/tag/', data=dict(tag=cases['tag']))
        validate(instance=resp.json, schema=POST_TAG_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['msg']

    @pytest.mark.parametrize('cases', delete_tag_cases())
    def test_delete(self, customer_client, cases):
        resp = customer_client.delete('/elebu/api/v1/tag/', data=dict(tag=cases['tag']))
        validate(instance=resp.json, schema=DELETE_TAG_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['msg']


@pytest.mark.usefixtures('admin_client')
class Test_UserApi:
    @pytest.mark.parametrize('cases', get_user_cases())
    def test_get(self, admin_client, cases):
        resp = admin_client.get(
            f"/elebu/api/v1/selfinfo/?num={cases['num']}&merchant_id={cases['merchant_id']}&keyword={cases['keyword']}&"
            f"tag={cases['tag']}&page={cases['page']}")
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message  ']

    @pytest.mark.parametrize('cases', put_user_cases())
    def test_put(self, admin_client, cases):
        resp = admin_client.put('/elebu/api/v1/selfinfo/', data={'pass': cases['pass'],
                                                                 'user_id': cases['user_id'],
                                                                 'selfintroduce': cases['selfintroduce']})
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', delete_user_cases())
    def test_delete(self, admin_client, cases):
        resp = admin_client.delete('/elebu/api/v1/selfinfo/', data=dict(del_thing=cases['del_thing'],
                                                                        del_thing_detail=cases['del_thing_detail'],
                                                                        user_id=cases['user_id']))
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']


@pytest.mark.usefixtures('merchant_client')
@pytest.mark.usefixtures('admin_client')
class Test_FoodApi:
    @pytest.mark.parametrize('cases', get_food_cases())
    def test_get(self, merchant_client, cases):
        resp = merchant_client.get(f"/elebu/api/v1/food/?num={cases['num']}&merchant_id={cases['merchant_id']}")
        if cases['num'] == 'all':
            validate(instance=resp.json, schema=GET_All_FOOD_SCHEMA)
        elif cases['num'] == 'self' or cases['merchant_id']:
            validate(instance=resp.json, schema=GET_SELF_OR_MERCHANT_FOOD_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', post_food_cases())
    def test_post(self, merchant_client, cases):
        resp = merchant_client.post('/elebu/api/v1/food/',
                                    data=dict(foodname=cases['foodname'], foodprice=cases['foodprice'],
                                              fooddesc=cases['fooddesc']))
        validate(instance=resp.json, schema=POST_PUT_DELETE_FOOD_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', put_food_cases())
    def test_put(self, admin_client, cases):
        resp = admin_client.put('/elebu/api/v1/food/',
                                data={'food_id': cases['food_id'], 'pass': cases['pass']})
        validate(instance=resp.json, schema=POST_PUT_DELETE_FOOD_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', delete_food_cases())
    def test_delete(self, admin_client, merchant_client, cases):
        client = merchant_client if cases['role'] == 2 else admin_client
        resp = client.delete('/elebu/api/v1/food/', data=dict(food_id=cases['food_id'], del_thing=cases['del_thing']))
        validate(instance=resp.json, schema=POST_PUT_DELETE_FOOD_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']


@pytest.mark.usefixtures('admin_client')
class Test_OrderApi:
    @pytest.mark.parametrize('cases', get_order_cases())
    def test_get(self, admin_client, cases):
        resp = admin_client.get(
            f"/elebu/api/v1/order/?user={cases['user']}&arrive={cases['arrive']}"
            f"&user_id={cases['user_id']}&role={cases['role']}")
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', put_order_cases())
    def test_put(self, admin_client, cases):
        resp = admin_client.put('/elebu/api/v1/order/',
                                data=dict(order_id=cases['order_id'], rider_salary=cases['rider_salary'],
                                          arrive=cases['arrive']))
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']


@pytest.mark.usefixtures('customer_client')
class Test_ZanApi:
    @pytest.mark.parametrize('cases', put_zan_cases())
    def test_put(self, customer_client, cases):
        resp = customer_client.put('/elebu/api/v1/zan/',
                                   data=dict(order_id=cases['order_id'], zan=cases['zan'], food_id=cases['food_id']))
        validate(instance=resp.json, schema=PUT_ZAN_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['msg']


@pytest.mark.usefixtures('admin_client')
class Test_FollowApi:
    @pytest.mark.parametrize('cases', get_follow_list_cases())
    def test_get_follow_list(self, admin_client, cases):
        resp = admin_client.get(f"/elebu/api/v1/follow/?follow_list={cases['follow_list']}")
        validate(instance=resp.json, schema=GET_FOLLOW_LIST_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', get_if_follow_cases())
    def test_get_if_follow(self, admin_client, cases):
        resp = admin_client.get(f"/elebu/api/v1/follow/?followed_id={cases['followed_id']}")
        validate(instance=resp.json, schema=GET_IF_FOLLOW_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', get_merchant_follow_cases())
    def test_get_merchant_follow(self, admin_client, cases):
        resp = admin_client.get(f"/elebu/api/v1/follow/?merchant_id={cases['merchant_id']}")
        validate(instance=resp.json, schema=GET_MERCHANT_FOLLOW)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', post_follow_cases())
    def test_post(self, admin_client, cases):
        resp = admin_client.post("/elebu/api/v1/follow/", data=dict(followed_id=cases['followed_id']))
        validate(instance=resp.json, schema=GET_MERCHANT_FOLLOW)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', delete_follow_cases())
    def test_delete(self, admin_client, cases):
        resp = admin_client.delete("/elebu/api/v1/follow/", data=dict(followed_id=cases['followed_id']))
        validate(instance=resp.json, schema=GET_MERCHANT_FOLLOW)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']


@pytest.mark.usefixtures('admin_client')
class Test_CommentApi:
    @pytest.mark.parametrize('cases', get_comment_cases())
    def test_get(self, admin_client, cases):
        resp = admin_client.get(f"/elebu/api/v1/comment/?num={cases['num']}&merchant_id={cases['merchant_id']}")
        print(cases)
        validate(instance=resp.json, schema=GET_COMMENT_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', post_comment_cases())
    def test_post(self, admin_client, cases):
        resp = admin_client.post("/elebu/api/v1/comment/",
                                 data=dict(sub=cases['sub'], rpy=cases['rpy'], comment=cases['comment'],
                                           merchant_id=cases['merchant_id']))
        validate(instance=resp.json, schema=POST_COMMENT_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', put_comment_cases())
    def test_put(self, admin_client, cases):
        resp = admin_client.put(
            "/elebu/api/v1/comment/", data=dict(comment_type=cases['comment_type'], comment_id=cases['comment_id']))
        validate(instance=resp.json, schema=PUT_DELETE_COMMENT_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', delete_comment_cases())
    def test_delete(self, admin_client, cases):
        resp = admin_client.delete(
            "/elebu/api/v1/comment/", data=dict(comment_type=cases['comment_type'], comment_id=cases['comment_id']))
        validate(instance=resp.json, schema=PUT_DELETE_COMMENT_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']


@pytest.mark.usefixtures('customer_client')
class Test_MessageApi:
    @pytest.mark.parametrize('cases', get_room_msg_cases())
    def test_get_room_msg(self, customer_client, cases):
        resp = customer_client.get(f"/elebu/api/v1/message/?room={cases['room']}&userid={cases['userid']}")
        validate(instance=resp.json, schema=GET_ROOM_MSG_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']

    @pytest.mark.parametrize('cases', get_self_msg_cases())
    def test_get_self_msg(self, customer_client, cases):
        resp = customer_client.get(f"/elebu/api/v1/message/?userid={cases['userid']}")
        validate(instance=resp.json, schema=GET_SELF_MSG_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['message']


@pytest.mark.usefixtures('admin_client')
class Test_NoticeApi:
    def test_get(self, admin_client):
        resp = admin_client.get('/elebu/api/v1/notice/')
        validate(instance=resp.json, schema=GET_NOTICE_SCHEMA)
        assert resp.json['status'] in (200, 404) and resp.json['message'] in ('success', 'not found')

    @pytest.mark.parametrize('cases', post_notice_cases())
    def test_post(self, cases):
        client = app.test_client()
        client.post('/user/login/', data=dict(username=cases['username'], password=cases['password']),
                    follow_redirects=True)

        resp = client.post('/elebu/api/v1/notice/',
                           data=dict(date=cases['date'], title=cases['title'], content=cases['content']))
        validate(instance=resp.json, schema=POST_NOTICE_SCHEMA)
        assert resp.json['status'] == cases['status'] and resp.json['message'] == cases['msg']
