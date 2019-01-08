#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = ""
from utils.logger.Log import Log
import yaml
import os


class FileOperation(object):
    def __init__(self, file_name: str):
        """
        文件操作类，传入文件地址，将文件读入缓存中备用
        """
        self.L = Log("FileOperation").logger
        self.fileName = file_name

    def get_file_details(self) -> dict:
        """
        将yaml按标准进行读取到缓存中，可以参照http://www.bejson.com/validators/yaml_editor/ 格式化效果
        将数据存放到data_file{}中
        :return:
        """
        self.L.critical("进入get_file_details")
        # 获取当前所处的文件夹上上一级文件夹的绝对路径
        try:
            cur_path = os.path.abspath('../..')
            # 获取yaml文件路径
            yaml_path = os.path.join(cur_path, self.fileName)
            # open方法打开直接读出来
            yaml_open = open(yaml_path, 'r', encoding='utf-8')
            # 用load方法转为字典,存放在data_files内
            data_file = yaml.load(yaml_open)
            self.L.debug('yaml文件解析为:%s' % data_file)
            return data_file
        except Exception as e:
            self.L.debug('yaml文件解析错误', e)

    def _format_checker(self):
        """
        检查文件请求数与断言数是否一致。
        :return:
        """
        data_files = {}
        try:
            data_file = self.get_file_details()
            for key in data_file:
                dict1 = data_file.get(key)
                data_keys = tuple(dict1.keys())
                # 判断yaml文件字段是否缺失
                if len(data_keys) == 3:
                    self.L.info("yaml文件接口:%s字段数正确" % key)
                    # 判断yaml文件字段名是否正确
                    if data_keys[0] == 'baseInfo':
                        if data_keys[1] == 'interfaceParameters':
                            if data_keys[2] == 'interfaceAsserts':
                                self.L.info("yaml文件接口:%s字段名正确" % key)
                                # 判断yaml文件内的interfaceParameters的case数和interfaceAsserts内的断言数是否对等
                                inf_para = dict1['interfaceParameters']
                                inf_asse = dict1['interfaceAsserts']
                                if len(inf_para) == len(inf_asse):
                                    self.L.info("yaml文件接口:%s interfaceParameters的case数和interfaceAsserts"
                                                "内的断言数相同" % key)
                                    # 判断yaml文件的baseInfo的必填项是否缺失
                                    base_info = dict1.get("baseInfo")
                                    if "requestMethod" in base_info:
                                        if "serverAddress" in base_info:
                                            self.L.info("yaml文件接口:%s baseInfo内的必填项未缺失" % key)
                                            # 将检查通过的接口请求数据放入data_files{}中
                                            data_files[key] = dict1
                                        elif "serverAddress" not in base_info:
                                            self.L.debug("yaml文件接口:%s baseInfo内的serverAddress字段缺失" % key)
                                    elif "requestMethod" not in base_info:
                                        self.L.debug("yaml文件接口:%s baseInfo内的requestMethod字段缺失" % key)
                                elif len(inf_para) != len(inf_asse):
                                    self.L.debug('yaml文件接口:%s interfaceParameters内case数与interfaceAsserts内断言'
                                                 '数不相等' % key)
                            elif data_keys[2] != 'interfaceAsserts':
                                self.L.debug('yaml文件中接口:%s interfaceAsserts字段缺失' % key)
                        elif data_keys[1] != 'interfaceParameters':
                            self.L.debug('yaml文件中接口:%s interfaceParameters字段缺失' % key)
                    elif data_keys[0] != 'baseInfo':
                        self.L.debug('yaml文件中接口:%s baseInfo字段缺失' % key)
                elif len(data_keys) != 3:
                    self.L.debug("yaml文件接口:%s 字段错误" % key)
            # 判断解析yaml文件获得的数据是否与检查通过的接口请求数据data_files是否相等,相等,则返回data_file{},
            # 不相等则抛出异常,且不返回data_file{}
            if len(data_file) == len(data_files):
                self.L.info("解析的yaml文件数据放入data_file{}中")
                return data_file
            elif len(data_file) != len(data_files):
                self.L.debug("接口请求缺失")
        except Exception as e:
            self.L.debug('请求异常:%s' % e)
