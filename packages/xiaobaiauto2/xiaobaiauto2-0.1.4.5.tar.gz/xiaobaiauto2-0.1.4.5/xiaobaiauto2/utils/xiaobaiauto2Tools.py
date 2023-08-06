#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'xiaobaiauto2Tools.py'
__create_time__ = '2020/9/23 23:14'

from typing import Optional
import argparse, os, zipfile
from jmespath import search
from json import loads, JSONDecodeError

def raw_handle(s: Optional[str] = ''):
    '''
    数据分割处理（单个请求放在一起）
    :param s:
    :return:
    '''
    s = s.strip()
    sLines = s.split('\n')
    _start_index = [i for i, _ in enumerate(sLines) if 'HTTP/' in _ or ':authority:' in _]
    _span_data = []
    for i, v in enumerate(_start_index):
        if v != _start_index[-1]:
            _span_data.append(sLines[v:_start_index[i+1]])
        else:
            _span_data.append(sLines[v:])
    # 数据分离(method、url、headers、data)
    result = []
    for request in _span_data:
        if 'HTTP/' in request[0]:
            _method = request[0].split(' ')[0]
            _headers = {}
            _headers_end = 0
            raw_header_data_list = request[1:]
            for _, j in enumerate(raw_header_data_list):
                _headers_end = _
                if '' == j:
                    break
                else:
                    _headers[j.split(': ')[0]] = j.split(': ')[1].strip()
            if raw_header_data_list.__len__() > _headers_end + 1:
                _data = ''.join([i for i in request[_headers_end + 1:] if i != ''])
            else:
                _data = ''
            _url = request[0].split(' ')[1]
            if '://' not in _url and '443' in _headers.get('Host'):
                _url = 'https://' + _headers.get('Host') + _url
            elif '://' not in _url and '443' not in _headers.get('Host'):
                _url = 'http://' + _headers.get('Host') + _url
            result.append(
                {
                    'method': _method,
                    'url': _url,
                    'headers': _headers,
                    'data': _data
                }
            )
        elif ':authority:' in request[0]:
            '''
            :authority: 域名
            :method:    方式
            :path:      地址
            :scheme:    协议
            '''
            _authority = request[0].split(':')[2].strip()
            _method = request[1].split(':')[2].strip()
            _path = request[2].split(':')[2].strip()
            _scheme = request[3].split(':')[2].strip()
            _url = _scheme + '://' + _authority + _path
            _headers = {}
            _headers_end = 0
            raw_header_data_list = request[4:]
            for _, j in enumerate(raw_header_data_list):
                _headers_end = _
                if '' == j:
                    break
                else:
                    _headers[j.split(': ')[0]] = j.split(': ')[1].strip()
            if raw_header_data_list.__len__() > _headers_end + 1:
                _data = ''.join([i for i in request[_headers_end + 1:] if i != ''])
            else:
                _data = ''
            result.append(
                {
                    'method': _method,
                    'url': _url,
                    'headers': _headers,
                    'data': _data
                }
            )
    return result

def har_handle(s: Optional[str] = ''):
    '''
    将har文件字符串，提取接口数据
    :param s:
    :return:
    '''
    search_result = search('log.entries[].request', loads(s))
    result = []
    for request in search_result:
        _method = request.get('method')
        _url = request.get('url')
        _headers = {}
        _data = ''
        for item in request.get('headers'):
            if item.get('name') not in [':method', ':path', ':authority', ':scheme']:
                _headers[item.get('name')] = item.get('value')
        if 'postData' in request.keys():
            if request.get('postData').get('mimeType') == 'application/json':
                _data = {}
                for item in request.get('postData').get('params'):
                    _data[item.get('name')] = item.get('value')
            else:
                for item in request.get('postData').get('params'):
                    _data += item.get('name') + '=' + item.get('value') + '&'
                _data = _data[:-1]
        result.append(
            {
                'method': _method,
                'url': _url,
                'headers': _headers,
                'data': _data
            }
        )
    return result

def convert(data: Optional[list], is_xiaobaiauto2: Optional[int] = 0) -> str:
    '''
    代码转换器
    :param data: {'method':'', 'url': '', 'headers': '', 'data': ''}
    :param is_xiaobaiauto2: 是否转为xiaobaiauto2库
    :param is_har: 是否是har文件
    :return:
    '''
    _code_top = '#! /usr/bin/env python\n'
    _code_pytest_import = 'from re import findall\n' \
                          'try:\n\timport pytest\n' \
                          '\timport requests\n' \
                          'except ModuleNotFoundError as e:\n' \
                          '\timport os\n' \
                          '\tos.system("pip install pytest")\n' \
                          '\tos.system("pip install requests")\n' \
                          '\timport pytest\n' \
                          '\timport requests\n\n'
    _code_xiaobaiauto2_import = 'try:\n\timport pytest\n' \
                                '\tfrom xiaobaiauto2.xiaobaiauto2 import api_action, PUBLIC_VARS\n' \
                                'except ModuleNotFoundError as e:\n' \
                                '\timport os\n' \
                                '\tos.system("pip install pytest")\n' \
                                '\timport pytest\n\n'
    _code_requests_import = 'from re import findall\n' \
                            'try:\n\timport requests\n' \
                            'except ModuleNotFoundError as e:\n' \
                            '\timport os\n' \
                            '\tos.system("pip install requests")\n' \
                            '\timport requests\n\n'
    _code_pytest_end = '\r# 脚本使用须知： ' \
                       '\r# pytest -s -v   运行当前目录所有test_*开头的脚本文件' \
                       '\r# pytest -s -v xxx.py 运行指定脚本文件' \
                       '\r# pytest -s -v --html=report.html  运行并将结果记录到HTML报告中' \
                       '\r# pytest其他运行方式参考https://pypi.org/project/xiaobaiauto2或官网说明'
    _code = ''
    for i, v in enumerate(data):
        if is_xiaobaiauto2 == 1:
            _code += f'''@pytest.mark.run(order={i + 1})\
                \rdef test_xiaobai_api_{i + 1}():\
                \r\t# 测试前数据准备 其中下方代码中{{变量名}}是需要在前面的接口返回值提取 \
                \r\theaders = {v.get('headers')}\
                \r\turl = '{v.get('url')}' \
                \r\tdata = '{v.get('data')}'\
                \r\tresponse = requests.request(method='{v.get('method')}', url=url, data=data, headers=headers)\
                \r\t# 测试后时间判断/提取\
                \r\t# assert response.status_code == 200  # 判断HTTP响应状态\
                \r\t# var_name = response.headers()[路径]  # 提取响应头数据\
                \r\t# global var_name # 设置全局变量\
                \r\tif 'application/json' in response.headers.get('Content-Type'):\
                \r\t\t# assert '预期结果' == response.json()[路径]  # 判断json响应体结果\
                \r\t\t# var_name = response.json()[路径]  # 提取json响应体数据\
                \r\t\t# var_name = response.headers()[路径]  # 提取响应头数据\
                \r\t\tprint(response.json())\
                \r\telse:\
                \r\t\t# assert '预期结果' in response.text # 判断字符串返回值结果 \
                \r\t\t# var_name = findall('正则表达式', response.text)[0] # 正则提取数据\
                \r\t\tprint(response.text)\n\n'''
        elif is_xiaobaiauto2 == 2:
            _code += f'''@pytest.mark.run(order={i + 1})\
                \rdef test_xiaobai_api_{i + 1}():\
                \r\t# 测试前数据准备\
                \r\theaders = {v.get('headers')}\
                \r\turl = '{v.get('url')}' \
                \r\tdata = '{v.get('data')}'\
                \r\tapi_action(\
                \r\t\tmethod='{v.get('method')}', url=url, data=data, headers=headers, verify=False,\
                \r\t\tjson_path='', json_assert='', contains_assert='', _re='', _re_var='')\
                \r\t# 表达式中json_path与json_assert为判断json结果是否符合预期值\
                \r\t# 表达式中contains_assert为模糊判断返回值是否包含预期结果\
                \r\t# 表达式中_re与_re_var为提取数据为下游接口提供数据支持\n\n'''
        else:
            _code += f'''\r# 测试前数据准备 其中下方代码中{{变量名}}是需要在前面的接口返回值提取 \
                \rheaders = {v.get('headers')}\
                \rurl = '{v.get('url')}' \
                \rdata = '{v.get('data')}'\
                \rresponse = requests.request(method='{v.get('method')}', url=url, data=data, headers=headers)\
                \r# 测试后数据判断/提取\
                \r# assert response.status_code == 200  # 判断HTTP响应状态\
                \r# var_name = response.headers()[路径]  # 提取响应头数据\
                \rif 'application/json' in response.headers.get('Content-Type'):\
                \r\t# assert '预期结果' == response.json()[路径]  # 判断json响应体结果\
                \r\t# var_name = response.json()[路径]  # 提取json响应体数据\
                \r\tprint(response.json())\
                \relse:\
                \r\t# assert '预期结果' in response.text # 判断字符串返回值结果 \
                \r\t# var_name = findall('正则表达式', response.text)[0] # 正则提取数据\
                \r\tprint(response.text)\n\n'''
    if is_xiaobaiauto2 == 1:
        return _code_top + _code_pytest_import + _code + _code_pytest_end
    elif is_xiaobaiauto2 == 2:
        return _code_top + _code_xiaobaiauto2_import + _code + \
               '\n# 使用公共变量的格式：\n# PUBLIC_VARS["变量名"][0][0]  获取响应头中第一个匹配值' \
               '\n# PUBLIC_VARS["变量名"][1][0]  获取响应体中第一个匹配值' + _code_pytest_end
    else:
        return _code_top + _code_requests_import + _code

def har_convert(data: Optional[str], is_xiaobaiauto2: Optional[int] = 0):
    '''
    har单文件转换
    :param data:
    :param is_xiaobaiauto2:
    :return:
    '''
    if data != '':
        return convert(data=har_handle(data), is_xiaobaiauto2=is_xiaobaiauto2)
    else:
        return ''

def raw_convert(raw: Optional[str], is_xiaobaiauto2: Optional[int] = 0) -> str:
    '''
    原文转换器
    :param raw:
    :param is_xiaobaiauto2: 是否转xiaobaiauto2库代码样例
    :return:
    '''
    if raw != '':
        return convert(data=raw_handle(raw), is_xiaobaiauto2=is_xiaobaiauto2)
    else:
        return ''

def file_convert(data: Optional[str], is_xiaobaiauto2: Optional[int], is_har: Optional[bool]):
    if is_har:
        return har_convert(data=data, is_xiaobaiauto2=is_xiaobaiauto2)
    else:
        return raw_convert(raw=data, is_xiaobaiauto2=is_xiaobaiauto2)

def compare_str(s0: Optional[str], s1: Optional[str], t: Optional[str]):
    '''
    比较两个字符串区别，暂时只考虑请求数据的不同，其他情况暂时忽略
    data = 'a=1&b=2&c=3'  字符串型
    data = '{'a':1, 'b': '0'}'  字典型
    data = '！@#￥%……&*'         文件内容型==字符串型
    :param s0: 字符串1
    :param s1: 字符串2
    :param t:  字符串是否含请求头
    :return:
    '''
    if 'application/json' in t:
        try:
            d0 = loads(s0)
            d1 = loads(s1)
        except JSONDecodeError as e:
            d0 = loads(s0.replace("'", '"'))
            d1 = loads(s1.replace("'", '"'))
        return compare_dict(d0, d1)
    else:
        if '=' in s0 and '=' in s1:
            # 分割参数
            sl0 = s0.split('&')
            sl0.sort()
            sl1 = s1.split('&')
            sl1.sort()
            result_str = ''
            for s_0, s_1 in zip(sl0, sl1):
                s_0l = s_0.split('=')
                s_1l = s_1.split('=')
                if s_0l[1] != s_1l[1]:
                    result_str += s_0l[0] + '=' + '{' + s_0l[0] +'}' + '&'
                else:
                    result_str += s_0 + '&'
            return result_str[:-1]

def compare_dict(d0: Optional[dict], d1: Optional[dict]) -> dict:
    '''
    比较两个字典数据
    :param d0:  字典对象1
    :param d1:  字典对象2
    :return:
    '''
    diff = d0.keys() & d1
    diffr = [(k, d0[k], d1[k]) for k in diff if d0[k] != d1[k]]
    diff_api = False
    if diffr.__len__() > 0:
        for v in diffr:
            if v[0] == 'method':
                diff_api = True
                break
            elif v[0] == 'url':
                diff_api = True
                break
            elif v[0] == 'headers':
                d0[v[0]] = compare_dict(v[1], v[2])
            else:
                try:
                    d0[v[0]] = compare_str(v[1], v[2], t=d0['headers']['content-type'])
                except KeyError as e:
                    try:
                        d0[v[0]] = compare_str(v[1], v[2], t=d0['headers']['Content-Type'])
                    except KeyError as e:
                        d0[v[0]] = compare_str(v[1], v[2], t='text')
    if diff_api:
        return {}
    else:
        d1.update(d0)
        return d1

def compare_har_convert(s0: Optional[str], s1: Optional[str], is_xiaobaiauto2: Optional[int] = 0):
    '''
    比较两个har文件字符串
    :param s0:
    :param s1:
    :return:
    '''
    result0 = har_handle(s0)
    result1 = har_handle(s1)
    result = []
    # 两个脚本数据雷同，记录条数一致
    for r0, r1 in zip(result0, result1):
        r = compare_dict(d0=r0, d1=r1)
        if r != {}:
            result.append(r)
        else:
            result.append(r0)
            result.append(r1)
    if result0.__len__() < result1.__len__():
        result.extend(result1[result0.__len__():])
    elif result1.__len__() < result0.__len__():
        result.extend(result0[result1.__len__():])
    if result.__len__() != 0:
        return convert(data=result, is_xiaobaiauto2=is_xiaobaiauto2)
    else:
        return ''

def api_raw(c: Optional[int], f: Optional[str], d: Optional[str], s: Optional[str], x: Optional[int]):
    if os.name == 'nt':
        step = '\\'
    else:
        step = '/'
    is_har = False
    if ',' not in f or c == 0:
        if os.path.isfile(f):
            raw_data = ''
            if os.path.splitext(f)[1] == '.saz':
                is_har = False
                raw_file_path = os.path.splitext(f)[0]
                zipfile.ZipFile(f).extractall(raw_file_path)
                raw_file_list = [i for i in os.listdir(raw_file_path + step + 'raw') if '_c.txt' == i[-6:]]
                for i in raw_file_list:
                    with open(raw_file_path + step + 'raw' + step + i, 'r') as fr:
                        raw_data += fr.read() + '\n\n\n'
                        fr.close()
                if os.path.isdir(raw_file_path):
                    try:
                        os.remove(raw_file_path)
                    except PermissionError as e:
                        pass
            elif os.path.splitext(f)[1] == '.har':
                is_har = True
                with open(f, 'r', encoding='utf-8') as fr:
                    raw_data += fr.read()
                    fr.close()
            elif os.path.splitext(f)[1] == '.txt':
                with open(f, 'r', encoding='utf-8') as fr:
                    is_har = False
                    raw_data += fr.read()
                    fr.close()
            code = file_convert(data=raw_data, is_xiaobaiauto2=x, is_har=is_har)
            if s:
                with open(s + '.py', 'w', encoding='utf-8') as fw:
                    fw.write(code)
                    fw.flush()
                    fw.close()
            else:
                with open(os.path.splitext(f)[0] + '.py', 'w', encoding='utf-8') as fw:
                    fw.write(code)
                    fw.flush()
                    fw.close()
        else:
            if f != '':
                if os.path.isfile(d + step + f):
                    raw_data = ''
                    if os.path.splitext(d + step + f)[1] == '.saz':
                        is_har = False
                        raw_file_path = os.path.splitext(d + step + f)[0]
                        zipfile.ZipFile(d + step + f).extractall(raw_file_path)
                        raw_file_list = [i for i in os.listdir(d + step + raw_file_path + step + 'raw') if '_c.txt' == i[-6:]]
                        for i in raw_file_list:
                            with open(d + step + raw_file_path + step + 'raw' + step + i, 'r') as fr:
                                raw_data += fr.read() + '\n\n\n'
                                fr.close()
                        if os.path.isdir(d + step + raw_file_path):
                            try:
                                os.remove(d + step + raw_file_path)
                            except PermissionError as e:
                                raise (e)
                    elif os.path.splitext(d + step + f)[1] == '.har':
                        is_har = True
                        with open(d + '/' + f, 'r', encoding='utf-8') as fr:
                            raw_data += fr.read()
                            fr.close()
                    elif os.path.splitext(d + step + f)[1] == '.txt':
                        with open(d + step + f, 'r', encoding='utf-8') as fr:
                            is_har = False
                            raw_data += fr.read()
                            fr.close()
                    code = file_convert(data=raw_data, is_xiaobaiauto2=x, is_har=is_har)
                    if s:
                        with open(d + step + s + '.py', 'w', encoding='utf-8') as fw:
                            fw.write(code)
                            fw.flush()
                            fw.close()
                    else:
                        with open(os.path.splitext(d + step + f)[0] + '.py', 'w', encoding='utf-8') as fw:
                            fw.write(code)
                            fw.flush()
                            fw.close()
            else:
                for f in [i for i in os.listdir(d) if os.path.splitext(i)[1] in ['.saz', '.har', '.txt']]:
                    raw_data = ''
                    if os.path.splitext(d + step + f)[1] == '.saz':
                        is_har = False
                        raw_file_path = os.path.splitext(d + step + f)[0]
                        zipfile.ZipFile(d + step + f).extractall(raw_file_path)
                        raw_file_list = [i for i in os.listdir(raw_file_path + step + 'raw') if
                                         '_c.txt' == i[-6:]]
                        for i in raw_file_list:
                            with open(raw_file_path + step + 'raw' + step + i, 'r') as fr:
                                raw_data += fr.read() + '\n\n\n'
                                fr.close()
                        if os.path.isdir(raw_file_path):
                            try:
                                os.remove(raw_file_path)
                            except PermissionError as e:
                                pass
                    elif os.path.splitext(d + step + f)[1] == '.har':
                        is_har = True
                        with open(d + step + f, 'r', encoding='utf-8') as fr:
                            raw_data += fr.read()
                            fr.close()
                    elif os.path.splitext(d + step + f)[1] == '.txt':
                        with open(d + step + f, 'r', encoding='utf-8') as fr:
                            is_har = False
                            raw_data += fr.read()
                            fr.close()
                    code = file_convert(data=raw_data, is_xiaobaiauto2=x, is_har=is_har)
                    if s:
                        with open(d + step + s + '.py', 'w', encoding='utf-8') as fw:
                            fw.write(code)
                            fw.flush()
                            fw.close()
                    else:
                        with open(os.path.splitext(d + step + f)[0] + '.py', 'w', encoding='utf-8') as fw:
                            fw.write(code)
                            fw.flush()
                            fw.close()
    elif ',' in f and c == 1:
        f_l = f.split(',')  # 一般是两个文件比较，目前支持两个，若有多个可以任意两个比较
        if f_l.__len__() > 1 and \
                os.path.isfile(f_l[0]) and \
                os.path.isfile(f_l[1]) and \
                os.path.splitext(f_l[0])[1] == '.har':
            ''' 暂时支持比较 *.har格式文件 '''
            data0 = ''
            data1 = ''
            with open(f_l[0], 'r', encoding='utf-8') as fr:
                data0 += fr.read()
                fr.close()
            with open(f_l[1], 'r', encoding='utf-8') as fr:
                data1 += fr.read()
                fr.close()
            code = compare_har_convert(s0=data0, s1=data1, is_xiaobaiauto2=x)
            if s is not None:
                with open(s + '.py', 'w', encoding='utf-8') as fw:
                    fw.write(code)
                    fw.flush()
                    fw.close()
            else:
                with open(os.path.splitext(f_l[0])[0] + '_' + os.path.splitext(f_l[1])[0] + '_compare.py',
                          'w', encoding='utf-8') as fw:
                    fw.write(code)
                    fw.flush()
                    fw.close()
        elif f_l.__len__() > 1 and \
                os.path.isfile(d + step + f_l[0]) and \
                os.path.isfile(d + step + f_l[1]) and \
                os.path.splitext(f_l[0])[1] == '.har':
            ''' 暂时支持比较 *.har格式文件 '''
            data0 = ''
            data1 = ''
            with open(d + step + f_l[0], 'r', encoding='utf-8') as fr:
                data0 += fr.read()
                fr.close()
            with open(d + step + f_l[1], 'r', encoding='utf-8') as fr:
                data1 += fr.read()
                fr.close()
            code = compare_har_convert(s0=data0, s1=data1, is_xiaobaiauto2=x)
            if s is not None:
                with open(d + step + s + '.py', 'w', encoding='utf-8') as fw:
                    fw.write(code)
                    fw.flush()
                    fw.close()
            else:
                with open(d + step + os.path.splitext(f_l[0])[0] + '_' + os.path.splitext(f_l[1])[0] + '_compare.py',
                          'w', encoding='utf-8') as fw:
                    fw.write(code)
                    fw.flush()
                    fw.close()

def cmd():
    arg = argparse.ArgumentParser(
        '小白科技·Python代码转换器·raw版·浏览器·Fiddler·Charles'
    )
    arg.add_argument('-c', '--compare',
                     type=int,
                     choices=(0, 1),
                     default=0,
                     help='比较两个har文件的区别,并转为python代码,0:不比较,1:比较,默认不比较')
    arg.add_argument('-f', '--file', type=str, help='支持txt|saz|har扩展名的raw数据文件')
    arg.add_argument('-d', '--dir',
                     type=str,
                     default='.',
                     help='批量转换指定目录下所有txt|saz|har扩展名的raw数据文件, 默认当前目录')
    arg.add_argument('-s', '--save', type=str, help='默认生成同名的.py文件,省略.py扩展名')
    arg.add_argument('-x', '--xiaobai',
                     type=int,
                     choices=(0, 1, 2),
                     default=0,
                     help='0:requests格式(默认),1:pytest格式,2:xiaobaiauto2格式')
    params = arg.parse_args()
    api_raw(c=params.compare, f=params.file, d=params.dir, s=params.save, x=params.xiaobai)

if __name__ == '__main__':
    cmd()