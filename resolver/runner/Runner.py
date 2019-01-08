#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "Zhang Pengfei"
from utils.logger.Log import Log
from resolver.selector.FileOperation import FileOperation
import requests
from utils.keywords.Dispatcher import Dispatcher
from utils.keywords.KeyGlobal import KeyGlobal
import string
import urllib.parse
import mimetypes
import json


class Runner(object):
    """
    获取yaml中的请求和断言，并调用Parser进行解析
    """
    def __init__(self):
        self.L = Log("Runner").logger
        self.key = KeyGlobal()
        self.key.set_global_key('data_current', '{}')
        self.key.set_global_key('data_last', '{}')
        self.p = Dispatcher()

    def do_request(self, filename):
        """
        1.按data_file中的接口数量和接口测试次数，组装请求，并检查结果(断言引用Parser进行关键字解析)
        2.需要记录当次测试，执行case的位置，第几个接口第几个步骤,每次执行完成后，将执行时的请求和响应封装到 data_current{}中
        3.将上一次请求的响应和结果封装到 data_last{}中
        4.执行请求前，需要检查请求中是否包含关键字
        :return:
        """
        self.L.critical("进入do_request")
        fop = FileOperation(filename)
        try:
            data_file = fop._format_checker()
        except Exception as e:
            raise Exception('当前文件异常')
        for interface_name in data_file.keys():
            self.L.critical('当前接口名字为: %s' % interface_name)
            data = data_file.get(interface_name)
            self.L.debug('当前接口是否运行: %s' % data.get('baseInfo').get('directExecution'))
            if data.get('baseInfo').get('directExecution') is True or data.get('baseInfo').get('directExecution') is None:
                self.L.info("当前接口的baseInfo数据存入全局变量baseInfo,值为: %s" % data.get('baseInfo'))
                self.key.set_global_key("baseInfo", data.get('baseInfo'))
                method = data.get('baseInfo').get('requestMethod')
                self.L.debug('当前接口请求方法: %s' % method)
                # 同一个接口在yaml不同层次使用时，用!!!做区分
                self.__choice_request(method, data, interface_name.split("!!!")[0])

    def __check_resp(self, data, index):
        """
        对一套断言进行解析并断言
        :param data: yaml文件中该接口的所有信息数据
        :param index: 该请求的第几套断言
        :return:
        """

        if data.get('interfaceAsserts')[index] is not None:

            for k, v in data.get('interfaceAsserts')[index].items():

                if isinstance(v, list):
                    if k.find('RECORD') < 0:
                        for j in v:
                            # todo 查找该关键字不做断言需要优化
                            try:
                                self.L.debug('断言是: %s, %s' % (self.p.key_dispatcher(k), self.p.key_dispatcher(j)))
                                assert self.p.key_dispatcher(k) == self.p.key_dispatcher(j)
                            except AssertionError:
                                self.L.error('\n期望值: %s\n返回值: %s' % (self.p.key_dispatcher(j), self.p.key_dispatcher(k)))
                    else:
                        self.L.info("该关键字不做断言,数据为 %s       %s:" % (k, v))
                        self.p.key_dispatcher(k, self.p.key_dispatcher(v))
                else:
                    if k.find('RECORD') < 0:
                        # todo 查找该关键字不做断言需要优化
                        try:
                            self.L.debug('断言是: %s, %s' % (self.p.key_dispatcher(k), self.p.key_dispatcher(v)))
                            assert self.p.key_dispatcher(k) == self.p.key_dispatcher(v)
                        except AssertionError:
                            self.L.error('\n期望值: %s\n返回值: %s' % (self.p.key_dispatcher(v), self.p.key_dispatcher(k)))
                    else:
                        self.L.info("该关键字不做断言,数据为 %s       %s:" % (k, v))
                        self.p.key_dispatcher(k, self.p.key_dispatcher(v))
        else:
            self.L.warning('yaml断言部分为空')

    def __get_data_params(self, index):
        """
        对请求的一套参数进行解析并拼接成dict
        :param index: 该请求的第几套参数
        :return: 返回dict
        """
        data_params = {}
        # try:
        for k, v in index.items():
            if k.find('RECORD') < 0:
                if isinstance(v, dict):
                    v_dict = {}
                    v_list = []
                    flag = 0
                    k = 1
                    for vk, vv in v.items():
                        vv = self.p.key_dispatcher(vv)
                        if isinstance(vv, list):
                            flag = 1
                            if k == 1:
                                for _ in vv:
                                    v_dict = {}
                                    v_list.append(v_dict)
                                k = k + 1
                            for i in range(len(vv)):
                                v_list[i][self.p.key_dispatcher(vk)] = self.p.key_dispatcher(vv[i])

                        else:
                            flag = 0
                            v_dict[self.p.key_dispatcher(vk)] = self.p.key_dispatcher(vv)
                    if flag == 0:
                        data_params[self.p.key_dispatcher(k)] = v_dict
                    else:
                        data_params[self.p.key_dispatcher(k)] = urllib.parse.quote(str(v_list), safe=string.printable)
                else:
                    k = self.p.key_dispatcher(k)
                    v = self.p.key_dispatcher(v)
                    data_params[k] = v
            else:
                self.p.key_dispatcher(k, self.p.key_dispatcher(v))
        # except Exception as e:
        #     self.L.error('解析请求参数错误: %s' % e)
        self.L.debug(data_params)
        return data_params

    def __choice_request(self, method, data, interface_name):
        self.L.debug('当前接口的HOST: %s' % data.get('baseInfo').get('serverAddress'))
        url = data.get('baseInfo').get('serverAddress') + interface_name
        self.L.debug('当前接口的Headers: %s' % data.get('baseInfo').get('requestHeaders'))
        headers = data.get('baseInfo').get('requestHeaders')
        index = 0
        for data_params in data.get('interfaceParameters'):
            self.L.info('当前接口请求解析前的参数: %s' % data_params)
            if data_params is not None:
                data_params = self.__get_data_params(data_params)
                self.L.info('当前接口请求解析后的参数: %s' % data_params)
            else:
                self.L.info('当前接口请求参数不需要解析')
            self.L.debug('写入全局变量data_last: %s' % self.key.get_global_value_by_key('data_current'))
            self.key.set_global_key("data_last", "%s" % self.key.get_global_value_by_key('data_current'))
            try:
                self.L.info("--------------------发送请求中--------------------")
                self.L.info("请求URL: %s" % url)
                self.L.info("参数: %s" % data_params)

                if method == 'POSTFILE':
                    file_path = str(list(data_params.values())[0])
                    file_key = list(data_params.keys())[0]
                    file_name = file_path.split("/")[-1:][0]
                    file_bin_data = open(file_path, 'rb')
                    content_type = str(mimetypes.types_map.get("." + file_path.split(".")[-1:][0], None))
                    files = {file_key: (file_name, file_bin_data, content_type)}
                    resp = requests.post(url=url, files=files)
                elif method == 'GET':
                    resp = requests.get(url=url, headers=headers, params=data_params)
                else:
                    resp = requests.post(url, headers=headers, data=data_params)
                self.L.info("--------------------请求已完成--------------------")
                self.L.info("请求返回: %s" % resp.text)
                if resp.status_code == 200:
                    try:
                        data_dict = {
                                        'req': data_params,
                                        'resp': json.loads(resp.text)
                                    }
                    except Exception as e:
                        self.L.error(e)
                        data_dict = {
                                        'req': data_params,
                                        'resp': resp.text
                                    }
                    self.L.debug('data_current: {"req": %s,"resp": %s}' % (data_params, resp.text))
                    self.key.set_global_key("data_current", data_dict)
                    self.__check_resp(data, index)
                elif str(resp.status_code)[0] == '5':
                    self.L.debug('服务器错误,状态为 %s' % str(resp.status_code))
                elif str(resp.status_code)[0] == '4':
                    self.L.debug('请求错误,状态为 %s' % str(resp.status_code))
                elif str(resp.status_code)[0] == '3':
                    self.L.debug('重定向请求,状态为 %s' % str(resp.status_code))
                else:
                    self.L.debug('不知名错误,状态为 %s' % str(resp.status_code))
            except Exception as e:
                self.L.error('请求异常 %s' % e)
            index += 1


if __name__ == '__main__':
    r = Runner()
    r.do_request("./testCase/user.yaml")
