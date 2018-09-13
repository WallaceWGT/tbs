#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

def handler_data(data):
    # 函数用于对请求过来的数据进行解析, 解析成一个字典的形式
    h_data = dict()
    try:
        info_data_list = data.split('&')
        for i in info_data_list:
            i_list = i.split('=')
            h_data[i_list[0]] = i_list[1]
    except IndexError:
        pass

    return h_data


if __name__ == '__main__':
    handler_data('')