#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth: wallace.wang

def fun(**kwargs):
    print 'aaa'
    obj = A()
    return obj

class A(object):
    def get(self):
        print '------'
        return 'ccc'