#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'xiaobaiauto2.py'
__create_time__ = '2020/7/2 18:20'

from xiaobaiauto2.utils.xiaobaiauto2db import DB
# from xiaobaiauto2.utils.xiaobaiCaptcha import find_text
from xiaobaiauto2.data.GLO_VARS import PUBLIC_VARS
from requests import request
from jmespath import search
from re import findall
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver  # , WebElement, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait  # , TimeoutException

def cmd2action(b=None, r=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    wait = WebDriverWait(b, PUBLIC_VARS['WebDriverWait'], PUBLIC_VARS['poll_frequency'])
    if r[0][0] == 1:
        if loc not in ('', None):
            if isinstance(b, WebDriver):
                e = wait.until(lambda b: b.find_element_by_xpath(loc))
                # e = b.find_element_by_xpath(loc)
                if '%s' in r[0][2] or '%d' in r[0][2]:
                    eval(r[0][2] % data)
                    if contains_assert:
                        assert contains_assert in eval(r[0][2] % data)
                    elif equal_assert:
                        assert equal_assert == eval(r[0][2] % data)
                else:
                    eval(r[0][2])
                    if contains_assert:
                        assert contains_assert in eval(r[0][2])
                    elif equal_assert:
                        assert equal_assert == eval(r[0][2])
    elif r[0][1] == 1:
        if isinstance(b, WebDriver):
            if '%s' in r[0][2] or '%d' in r[0][2]:
                eval(r[0][2] % data)
                if contains_assert:
                    assert contains_assert in eval(r[0][2] % data)
                elif equal_assert:
                    assert equal_assert == eval(r[0][2] % data)
            else:
                eval(r[0][2])
                if contains_assert:
                    assert contains_assert in eval(r[0][2])
                elif equal_assert:
                    assert equal_assert == eval(r[0][2])
    else:
        if '%s' in r[0][2] or '%d' in r[0][2]:
            eval(r[0][2] % data)
            if contains_assert:
                assert contains_assert in eval(r[0][2] % data)
            elif equal_assert:
                assert equal_assert == eval(r[0][2] % data)
        else:
            eval(r[0][2])
            if contains_assert:
                assert contains_assert in eval(r[0][2])
            elif equal_assert:
                assert equal_assert == eval(r[0][2])

def action(app_type=1, b=None, cmd=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    '''
    操作方法
    :param app_type: 操作对象类型1为web，2为app
    :param b: 操作对象
    :param cmd: 操作命令
    :param loc: 操作路径
    :param data: 操作数据
    :param contains_assert: 包含校验
    :param equal_assert: 相等校验
    :return:
    '''
    if b is not None:
        db = DB()
        r = db.select(f"select is_element,is_driver,code\
                      from keyword\
                      where testtype like '%{app_type}%' and command like '%{cmd}%' or key='{cmd}' limit 1;")
        cmd2action(b, r, loc, data, contains_assert, equal_assert)

def web_action(b=None, cmd=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    action(app_type=1, b=b, cmd=cmd, loc=loc, data=data, contains_assert=contains_assert, equal_assert=equal_assert)

def app_aciton(b=None, cmd=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    action(app_type=2, b=b, cmd=cmd, loc=loc, data=data, contains_assert=contains_assert, equal_assert=equal_assert)

def api_action(method='POST', url='', headers=None, params=None, data=None,json_path=None, json_assert=None,
               contains_assert=None, _re='', _re_var='', verify=True, **kwargs):
    '''
    接口操作方法
    :param method: 接口请求方式
    :param url: 接口地址
    :param headers: 接口请求头
    :param params: 接口请求参数（GET）
    :param data: 接口请求数据(非GET)
    :param json_path: json校验路径
    :param json_assert: json校验内容
    :param contains_assert: 包含校验
    :param _re: 提取正则表达式
    :param _re_var: 提取数据变量名
    :param verify: 安全校验
    :param kwargs:
    :return:
    '''
    if method.lower() == 'get':
        res = request(method=method, url=url, headers=headers, params=params, verify=verify, kwargs=kwargs)
    else:
        res = request(method=method, url=url, headers=headers, data=data, verify=verify, kwargs=kwargs)
    global PUBLIC_VARS
    if json_path:
        assert json_assert == search(json_path, res.json())
    elif contains_assert:
        assert contains_assert in res.text
    if _re != '' and _re_var != '':
        PUBLIC_VARS[_re_var] = []
        PUBLIC_VARS[_re_var][0] = findall(_re, res.headers.__str__())
        PUBLIC_VARS[_re_var][1] = findall(_re, res.text)