#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'client.py'
__create_time__ = '2020/9/18 13:50'

from typing import Optional
from requests import request, RequestException
from jmespath import search
from re import findall
import pysnooper

class BaseRequest(object):
    def __init__(self, title: Optional[str] = ''):
        self.title = title
        self.env = {}

    def __call__(self, func):
        def wrapper(**kwargs):
            test = {}
            env_data = {}
            if 'before' in kwargs.keys():
                for params, value in kwargs.items():
                    if params in ['before', 'after']:
                        continue
                    else:
                        k_list = findall('\{(.+?)\}', str(value))
                        if k_list.sort() == list(dict(kwargs['before']).keys()).sort():
                            kwargs[params] = str(value).format_map(kwargs['before'])
                        else:
                            for k in k_list:
                                if k in dict(kwargs['before']).keys():
                                    kwargs[params] = str(value).replace('{' + k +'}', kwargs['before'][k])
                kwargs.pop('before')
            if 'after' in kwargs.keys():
                if 'test' in dict(kwargs['after']).keys():
                    test = kwargs['after']['test']
                if 'env' in dict(kwargs['after']).keys():
                    env_data = kwargs['after']['env']
                kwargs.pop('after')
            '''
            [
                {
                'api_title': '注册接口',
                'api_id': 'register',
                'before': {
                    'def_env':{
                        'remark':'方法变量，范围最小',
                        'baseUrl0': 'http://dev.xiaobai.com', 
                        'baseUrl1': 'https://test.xiaobai.com',
                        'baseUrl2': 'https://pord.xiaobai.com',
                        'version': ['1.0', '2.0', '3.0'],
                    },
                    'class_env':{
                        'remark':'类变量，范围较大',
                        'baseUrl0': 'http://dev.xiaobai.com', 
                        'baseUrl1': 'https://test.xiaobai.com',
                        'baseUrl2': 'https://pord.xiaobai.com',
                        'version': ['1.0', '2.0', '3.0'],
                    },
                    'global_env': {
                        'remark':'全局变量又称公共变量，范围最大',
                        'baseUrl0': 'http://dev.xiaobai.com', 
                        'baseUrl1': 'https://test.xiaobai.com',
                        'baseUrl2': 'https://pord.xiaobai.com',
                        'version': ['1.0', '2.0', '3.0'],
                    },
                    
                },
                'request':{
                    'method': 'POST',
                    'headers': {'Content-Type': 'application/json'},
                    'url': '$[api_id=='register'].before.def_env.baseUrl0',
                    'paramer': 'q=xiaobai&version=$[api_id=='register'].before.def_env.version[0]',
                    'data': '{'a': 'xiaobai', 'version': $[api_id=='register'].before.def_env.version[0]}'
                },
                'after': {
                    'test': {
                        'json': [{'at':'body', 'path': 'code', 'value': 'xiaobai'}], 
                        'match': [{'at':'body', 'path': 0, 'value': ['xiaobai']}]
                    },
                    'env': {
                        'json': [{'at':'body', 'path': 'code', 'name': 'xiaobai'}], 
                        'match': [{'at':'body', 'path': 'ni(.+?)hao', 'name': 'xiaobai'}]
                    }
                }
            },
            {
                'api_title': '登录接口',
                'api_id': 'login',
                'before': {
                    'def_env':{
                        'remark':'方法变量，范围最小',
                        'baseUrl0': 'http://dev.xiaobai.com', 
                        'baseUrl1': 'https://test.xiaobai.com',
                        'baseUrl2': 'https://pord.xiaobai.com',
                        'version': ['1.0', '2.0', '3.0'],
                    },
                    'class_env':{
                        'remark':'类变量，范围较大',
                        'baseUrl0': 'http://dev.xiaobai.com', 
                        'baseUrl1': 'https://test.xiaobai.com',
                        'baseUrl2': 'https://pord.xiaobai.com',
                        'version': ['1.0', '2.0', '3.0'],
                    },
                    'global_env': {
                        'remark':'全局变量又称公共变量，范围最大',
                        'baseUrl0': 'http://dev.xiaobai.com', 
                        'baseUrl1': 'https://test.xiaobai.com',
                        'baseUrl2': 'https://pord.xiaobai.com',
                        'version': ['1.0', '2.0', '3.0'],
                    },
                    
                },
                'request':{
                    'method': 'POST',
                    'headers': {'Content-Type': 'application/json'},
                    'url': '$[api_id=='register'].before.def_env.baseUrl0',
                    'paramer': 'q=xiaobai&version=$[api_id=='register'].before.def_env.version[0]',
                    'data': '{'a': 'xiaobai', 'version': $[api_id=='register'].before.def_env.version[0]}'
                },
                'after': {
                    'test': {
                        'json': [{'at':'body', 'path': 'code', 'value': 'xiaobai'}], 
                        'match': [{'at':'body', 'path': 0, 'value': ['xiaobai']}]
                    },
                    'env': {
                        'json': [{'at':'body', 'path': 'code', 'name': 'xiaobai'}], 
                        'match': [{'at':'body', 'path': 'ni(.+?)hao', 'name': 'xiaobai'}]
                    }
                }
            }
            ]
            at的值：body,headers,status
            '''
            try:
                res = request(**kwargs)
                if test != {}:
                    if 'json' in test.keys():
                        for j in test['json']:
                            j = dict(j)
                            if j.get('at') == 'body':
                                assert j.get('value') == search(j.get('path'), res.json())
                            elif j.get('at') == 'headers':
                                assert j.get('value') == search(j.get('path'), res.headers)
                            elif j.get('at') == 'status':
                                raise ('状态码不能使用json格式')
                    elif 'match' in test.keys():
                        for m in test['json']:
                            m = dict(m)
                            if m.get('at') == 'body':
                                assert m.get('value') in res.text
                            elif m.get('at') == 'headers':
                                assert m.get('value') in res.headers.__str__()
                            elif m.get('at') == 'status':
                                assert m.get('value') in res.status_code
                    else:
                        exit(-1)
                        raise ('参数有误')
                if env_data != {}:
                    if 'json' in test.keys():
                        for j in test['json']:
                            j = dict(j)
                            if j.get('at') == 'body':
                                self.env[j.get('name')] = search(j.get('path'), res.json())
                            elif j.get('at') == 'headers':
                                self.env[j.get('name')] = search(j.get('path'), res.headers)
                            elif j.get('at') == 'status':
                                self.env[j.get('name')] = res.status_code
                    elif 'match' in test.keys():
                        for m in test['json']:
                            m = dict(m)
                            if m.get('at') == 'body':
                                self.env[m.get('name')] = findall(m.get('path'), res.text)
                            elif m.get('at') == 'headers':
                                self.env[m.get('name')] = findall(m.get('path'), res.headers.__str__())
                            elif m.get('at') == 'status':
                                self.env[m.get('name')] = res.status_code
                    else:
                        exit(-1)
                        raise ('参数有误')
            except RequestException as e:
                exit(-1)
                raise ('请求参数有误', e)
            print(self.title, '执行完测试')
            return func()
        return wrapper