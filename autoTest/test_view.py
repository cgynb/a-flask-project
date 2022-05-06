# -*- coding: utf-8 -*-
# @Time    : 2022/4/28 17:31
# @Author  : CGY
# @File    : test_view.py
# @Project : NewWaiMai 
# @Comment : view_test
import pytest
from app import app
from funcs import *


@pytest.mark.usefixtures('customer_client')
class TestUser:
    @pytest.mark.parametrize('cases', login_cases())
    def test_login(self, cases):
        client = app.test_client()
        resp = client.post('/user/login/', data={'username': cases['username'], 'password': cases['password']},
                           follow_redirects=True)
        assert f"<script>Materialize.toast('{cases['msg']}', 4000)</script>" in resp.text

    def test_logout(self):
        client = app.test_client()
        client.post('/user/login/', data=dict(username='cgy', password=111111),
                    follow_redirects=True)
        resp = client.get('/user/logout/', follow_redirects=True)
        assert "<script>Materialize.toast('退出登录', 4000)</script>" in resp.text

    @pytest.mark.parametrize('cases', change_username_cases())
    def test_change_username(self, customer_client, cases):
        customer_client.post('/user/login/', data=dict(username='cgy', password=111111),
                             follow_redirects=True)
        resp = customer_client.post('/user/change_username/', data=dict(newusername=cases['newusername']),
                                    follow_redirects=True)
        assert f"<script>Materialize.toast('{cases['msg']}', 4000)</script>" in resp.text


@pytest.mark.usefixtures('merchant_client')
class TestFood:

    def test_index(self, merchant_client):
        resp = merchant_client.get('/')
        assert '首页' in resp.text

    def test_upload_food(self, merchant_client):
        resp = merchant_client.get('/food/')
        assert '上架食品' in resp.text

    def test_shop(self, merchant_client):
        resp = merchant_client.get('/shop/')
        assert '店铺' in resp.text


@pytest.mark.usefixtures('merchant_client')
class TestChat:
    def test_chatroom(self, merchant_client):
        resp = merchant_client.get('/user/chatlist/', follow_redirects=True)
        assert '聊天列表' in resp.text

    @pytest.mark.parametrize('cases', chatroom_cases())
    def test_charlist(self, merchant_client, cases):
        resp = merchant_client.get(f"/chat/?orderid={cases['orderid']}", follow_redirects=True)
        assert cases['title'] in resp.text


@pytest.mark.usefixtures('admin_client')
class TestAdmin:
    def test_admin(self, admin_client):
        admin_client.post('/user/login/', data=dict(username='admin_cgy', password=111111),
                          follow_redirects=True)
        resp = admin_client.get('/admin/')
        assert '管理界面' in resp.text
