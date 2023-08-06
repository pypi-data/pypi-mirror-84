#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'utils.py'
__create_time__ = '2020/11/2 19:15'

from yaml import load_all, dump_all

class APIHandleBase(object):
    def convert(self):
        ''' convert xiaobaiauto2's class  '''
        pass

    def json2yaml(self):
        ''' json file convert to yaml file '''
        pass

    def yaml2json(self):
        ''' yaml file convert to json file '''

    def cmdRun(self):
        ''' pytest run '''
        pass

    def yamlRun(self):
        ''' yaml file run '''
        pass

    def jsonRun(self):
        ''' json file run '''
        pass

class ApiHandle(APIHandleBase):
    def json2yaml(self):
        pass