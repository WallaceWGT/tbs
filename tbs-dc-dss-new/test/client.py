#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

import requests

def auth_test():
    data = requests.request(
        method='post',
        # 登入认证时的url已经请求的数据
        url='http://127.0.0.1:8005/auth',
        data={'appID': '123456','authKey': 'qwe123'},
    )
    print data.text


def server_test():
    data = requests.request(
        method='post',
        # 数据操作时的url以及请求数据
        url='http://127.0.0.1:8005/operate',
        headers={'token': '888', 'appID': '123456'},
        # apiInstance:  模块名   get: 操做数据的方式   params: 参数名
        data={'api': 'test.get', 'params1': 'aaa', 'params2': 'bbb'}
    )
    print data.text


if __name__ == '__main__':
    # auth_test()
    server_test()