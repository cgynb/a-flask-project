from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest


class Test_Chatroom:
    def test_send(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:5000/user/login/')
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys('cgy')
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('111111')
        driver.find_element(By.XPATH, '/html/body/div[1]/form/div[4]/div/button').click()
        driver.get('http://127.0.0.1:5000/chat/?orderid=4954209wSnTaQ4')
        driver.find_element(By.XPATH, '//*[@id="last_name"]').send_keys('5.17test')
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/a').click()
        driver.close()

    def test_get_msg(self):
        from app import app
        client = app.test_client()
        client.username = 'cgy'
        client.password = 111111
        client.role = 1
        client.post('/user/login/', data=dict(username=client.username, password=client.password),
                    follow_redirects=True)
        resp = client.get(f"/elebu/api/v1/message/?room=4954209wSnTaQ4&userid=4")
        lastMsg = resp.json['data'][len(resp.json['data'])-1]['message']
        assert lastMsg == '5.17test'
