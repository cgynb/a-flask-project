# -*- coding: utf-8 -*-
# @Time    : 2022/4/29 0:25
# @Author  : CGY
# @File    : run.py
# @Project : NewWaiMai 
# @Comment : pytest run file
import pytest
import os

if __name__ == '__main__':
    pytest.main(
        ['-sv', '--cov=C:/Users/cgy/Desktop/NewWaiMai', '--cov-report=html', '--alluredir', 'results'])
    os.system('allure generate results -o reports')
