#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "xin.heng@worldfarm.com"


import requests
import json
import mimetypes
import urllib.parse
from utils.logger.Log import Log


class SendRequest(object):

    def __init__(self):
        """
        请求类初始化本类日志
        """
        self.L = Log("SendRequest").logger

    @staticmethod
    def _json_format(data):
        if isinstance(data, str):
            json_str = json.loads(data)
            return json.dumps(json_str, ensure_ascii=False, sort_keys=True,
                              indent=2, separators=(',', ': '))
        elif isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False, sort_keys=True,
                              indent=2, separators=(',', ': '))

    def post(self, url: str, body: object, headers: dict = None, cookies=None) -> str:
        """
        发送POST请求
        :param url: 包括请求协议与请求路径的地址
        :param body: 请求报文消息内容
        :param headers: 请求报文头
        :param cookies: 请求cookie
        :return: python3默认为bytes, 统一返回decode之后的str
        """
        client = requests.session()
        response = client.post(url=url, data=body, headers=headers, cookies=cookies).content.decode('utf-8')
        # todo: 暂时未做各响应码的判断
        self.L.debug("请求地址: %s" % url)
        self.L.debug("请求参数:\n%s" % self._json_format(body))
        self.L.debug("响应内容:\n%s" % self._json_format(response))
        return response

    def get(self, url: str, headers: dict = None) -> str:
        """
        发送GET请求
        :param url: 包括请求协议与请求参数的地址
        :param headers: 请求报文头
        :return: python3默认为bytes, 统一返回decode之后的str
        """
        client = requests.session()
        response = client.get(url=url, headers=headers).content.decode('utf-8')
        # todo: 暂时未做各响应码的判断
        self.L.debug("请求地址: %s" % url)
        self.L.debug("响应内容:\n%s" % self._json_format(response))
        return response

    def post_file(self, url: str, file_path: str, file_key: str, data_dict: dict = None) -> str:
        """
        发送POST文件请求
        :param url: 包括请求协议与请求路径的地址
        :param file_path: 文件的全路径
        :param file_key: 传文件的键名
        :param data_dict: 报文消息体内容
        :return: python3默认为bytes, 统一返回decode之后的str
        """
        file_name = file_path.split("/")[-1:][0]
        file_bin_data = open(file_path, 'rb')
        content_type = str(mimetypes.types_map.get("." + file_path.split(".")[-1:][0], None))
        encode_file_name = urllib.parse.quote(file_name, safe='&?=:/', encoding='UTF-8', errors=None)
        files = {file_key: (encode_file_name, file_bin_data, content_type)}
        response = requests.post(url=url, data=data_dict, files=files).content.decode('utf-8')
        # todo: 暂时未做各响应码的判断, 后期优化到post方法中
        self.L.debug("请求地址: %s" % url)
        self.L.debug("文件: %s" % file_path)
        self.L.debug("请求参数:\n%s" % self._json_format(data_dict))
        self.L.debug("响应内容:\n%s" % self._json_format(response))
        return response


if __name__ == '__main__':
    send_request = SendRequest()
    data_body = {'mobile': 18380581404, 'verifyCode': 8888, 'deviceType': 1,
                 'deviceId': 'unknown', 'accountType': 'CUSTOMER', 'appId': 'MS_APP'}
    emp_data = {"appId": "MS_SYS",
                "deviceType": "WEB",
                "account": '18382373185',
                "password": 'o8h85G',
                "deviceId": "zhangpengfei"}
    login = send_request.post("http://dev.ms.passport.sjnc.com/admin/service/account-login", body=emp_data)
    json_login = json.loads(login)
    token = json_login['content']['token']
    device_id = json_login['content']['deviceId']
    # send_request.get("http://dev.ms.order.sjnc.com/v2/api-docs")
    send_request.post_file("http://dev.ms.kbms.sjnc.com/admin/plant/import?_tk_=%s&_deviceId_=%s"
                           % (token, device_id), file_key="file", file_path="/Users/hengxin/植物特性表.xlsx")

