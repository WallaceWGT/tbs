#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from config.settings import SECRET_KEY


class AuthToken(object):

    # 用于处理token信息流程：
    # 1、更加给定的用户信息生成token
    # 2、保存生成的token，以便于后面验证
    # 3、对用户请求多来的token进行验证：
    #   验证成功--->继续执行后面操作
    #   验证失败--->返回状态码通知client带用户信息来重新生成token

    def __init__(self, app_id):
        """
        初始化数据
        :param app_id:
        """
        self.app_id = app_id
        # 结合配置文件的盐与app_id一起构造出新的盐
        self._SECRET_KEY = self.app_id + SECRET_KEY

    # token生成,expiration是过期时间,默认为3600s
    def generate_token(self, expiration=3600):
        token_obj = Serializer(self._SECRET_KEY, expires_in=expiration)
        token = token_obj.dumps({'app_id': self.app_id})
        return token

    # 认证token
    def verify_auth_token(self, token):
        token_obj = Serializer(self._SECRET_KEY)
        try:
            token_obj.loads(token)
        except SignatureExpired:
            msg = 'valid token, but expired'
            return msg
        except BadSignature:
            msg = 'Invalid token'
            return msg
        return True

if __name__ == '__main__':
    token_obj = AuthToken('123')
    token = token_obj.generate_token(30)

    print token  # eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNjczMTAyNywiaWF0IjoxNTM2NzMwOTk3fQ.eyJhcHBfaWQiOiIxMjMifQ.-p-kdLSJsX-6Oxk3fF6Tp6D_Rvk6h3O1rmu18e6o9Yo

    token_obj1 = AuthToken('123')  #返回True
    # token_obj1 = AuthToken('12')     #Invalid token
    action = token_obj1.verify_auth_token('eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNjczMTAyNywiaWF0IjoxNTM2NzMwOTk3fQ.eyJhcHBfaWQiOiIxMjMifQ.-p-kdLSJsX-6Oxk3fF6Tp6D_Rvk6h3O1rmu18e6o9Yo')
    print action
