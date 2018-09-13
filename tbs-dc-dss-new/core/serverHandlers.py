#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

import imp
import json
from tornado import web

from com.utils.MyLog import MyLog
from utils.handlerData import handler_data
from utils.auth import AuthToken


class AuthHandler(web.RequestHandler):
    def initialize(self):
        """
        identity_data:是请求时的用户信息
        response_data:用于返回给请求端的数据
        identity_action:标识的是认证的结果，成功则为True默认为False
        :return:
        """
        self.identity_data = dict()
        self.response_data = {'status': None, 'access_token': None, 'msg': None}
        self.identity_action = False
        self.log = MyLog(path='../log/', name='login')

    # 数据处理和认证
    def prepare(self):
        self.identity_data = handler_data(self.request.body)
        if len(self.identity_data) == 0:
            self.write('Please carried valid data ')
        self._identity_auth()
        self._generate_response_data()

    # 认证逻辑
    def _identity_auth(self):
        # 这里的密码保存在数据的密码进行匹配/需要连接数据库
        # info = self._get_info()
        info = {'appID': '123456', 'authKey': 'qwe123'}
        if self.identity_data.get('appID') == info['appID'] and \
                        self.identity_data.get('authKey') == info['authKey']:
            self.identity_action = True
            log_msg = '%s login successful' % self.identity_data.get('appID')
            self.log.info(log_msg)
        else:
            if self.identity_data.get('appID') is None or self.identity_data.get('authKey') is None:
                log_msg = 'Request parameter errors'
                self.log.warning(log_msg)
                self.write('Request parameter errors, please provide the correct request parameters')
            log_msg = 'login fails, UserID or authKey is error '
            self.response_data['msg'] = 'appID or authKey is error'
            self.log.warning(log_msg)

    def _generate_response_data(self):
        if self.identity_action is True:
            token = AuthToken(self.identity_data.get('appID')).generate_token()
            self.response_data['status'] = 8000
            self.response_data['access_token'] = token
            self.response_data['msg'] = 'Identity success'
        else:
            self.response_data['status'] = 8004

    # 返回数据
    def post(self, *args, **kwargs):
        print '数据返回'
        self.write(json.dumps(self.response_data))


class BaseHandler(web.RequestHandler):
    def initialize(self):
        self.request_data = dict()
        self.response_data = {'status': None, 'data': None, 'msg': None}
        self.auth_status = None

    def prepare(self):
        # 认证token信息

        token = self.request.headers.get('Token')
        self.app_id = self.request.headers.get('appID')
        if not token or not self.app_id:
            self.write('Request parameter errors, please provide the correct request parameters')
        self.request_data = handler_data(self.request.body)
        self.log = MyLog(path='../log/', name='server')
        # self.auth_status = AuthToken(self.app_id).verify_auth_token(token)
        self.auth_status=True  # 测试获取数据使用

        if self.auth_status is not True:
            self.response_data['status'] = 9004
            self.response_data['msg'] = self.auth_status
            log_msg = '%s authentication failure' % self.app_id
            self.log.warning(log_msg)
            self.write(json.dumps(self.response_data))
        else:
            pass


class ServerHandler(BaseHandler):

    def post(self, *args, **kwargs):
        try:
            api_module, method = tuple(self.request_data.pop('api').split('.'))
            parameters = self.request_data
        except KeyError, e:
            msg = 'Request parameter errors, please provide the correct request parameters!'
            self.response_data['msg'] = msg
            self.response_data['status']=7004
            self.log.error(msg)
            self.write(self.response_data)
        self._specific_operate(api_module, method, **parameters)
        self.write(json.dumps(self.response_data))

    def _specific_operate(self, api_module, method, **kwargs):
        """
        这里是根据提供的数据进行动态的导入模块，注意这里导入模块是要根据文件路径来导入
        导入后根据提供的method来操纵数据并得到返回值
        :param data:
        :return:
        """
        import os
        try:
            # 根据提供的api_name动态导入模块
            # path = os.sep.join([os.path.dirname(os.path.dirname(os.path.abspath(__name__))),api_module+'.py'])

            module_li = imp.load_source('mymode', r'G:\project_code\tbs-dc-dss-new\test\test1.py')
            obj = module_li.fun(**kwargs)
            data_result = getattr(obj, method)
            operate_data = data_result()
            self.response_data['data'] = operate_data
            self.response_data['status'] = 7000
            self.response_data['msg'] = 'operate success'
            log_msg = '%s %s operation is successful, object is %s' % (self.app_id, method, api_module)
            self.log.info(log_msg)
        except (TypeError, AttributeError, ImportError, KeyError), e:
            if isinstance(e, KeyError):
                e = 'Params is Invalid'
            self.response_data['msg'] = str(e)
            self.response_data['status'] = 7004
            log_msg = '%s %s operation is fails,by operated object is %s, the reason is %s' %\
                      (self.app_id, method, api_module, e)
            self.log.error(log_msg)