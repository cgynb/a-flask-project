import pytest
from app import app


@pytest.fixture(scope='class')
def merchant_client():
    client = app.test_client()
    client.username = 'merchant_cjl'
    client.password = 111111
    client.role = 2
    client.post('/user/login/', data=dict(username=client.username, password=client.password), follow_redirects=True)
    yield client
    client.get('/user/logout/', follow_redirects=True)


@pytest.fixture(scope='class')
def customer_client():
    client = app.test_client()
    client.username = 'cgy'
    client.password = 111111
    client.role = 1
    client.post('/user/login/', data=dict(username=client.username, password=client.password), follow_redirects=True)
    yield client
    client.get('/user/logout/', follow_redirects=True)


@pytest.fixture(scope='class')
def rider_client():
    client = app.test_client()
    client.username = 'rider_cqh'
    client.password = 111111
    client.role = 3
    client.post('/user/login/', data=dict(username=client.username, password=client.password), follow_redirects=True)
    yield client
    client.get('/user/logout/', follow_redirects=True)


@pytest.fixture(scope='class')
def admin_client():
    client = app.test_client()
    client.username = 'admin_cgy'
    client.password = 111111
    client.role = 4
    client.post('/user/login/', data=dict(username=client.username, password=client.password), follow_redirects=True)
    yield client
    client.get('/user/logout/', follow_redirects=True)
