#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "luyao.yang@worldfarm.com"

from utils.logger.Log import Log
from utils.basic.UniversalDataOperation import UniversalDataOperation
global_dict = {}


class KeyGlobal(object):
    """
    1.RECORD 关键字，将指定的值，存储为全局变量，在任意test case均可直接调用
    2.READ 关键字，读取存储的全局变量
    数据存放到 data_global{} 中
    """

    def __init__(self):
        global global_dict
        self.L = Log("KeyGlobal").logger

    def set_global_key(self, key, value):
        """
        实现RECORD，将value，存储为key的值，全局可用data_global
        :param key:
        :param value:
        :return:
        """
        global_dict[key] = value
        self.L.info("{%s: %s}已设置" % (key, value))

    def get_global_value_by_key(self, key: str, key_type: str = ""):
        """
        给REQUEST\LREQUEST\RESPONSE\LRESPONSE 提供检查方法
        :param key_type:
        :param key:
        :return:
        """
        try:
            if key_type == "REQUEST":
                value = UniversalDataOperation().get_dicts_value_by_key_path(global_dict["data_current"]["req"], key)
            elif key_type == "LREQUEST":
                value = UniversalDataOperation().get_dicts_value_by_key_path(global_dict["data_last"]["req"], key)
            elif key_type == "RESPONSE":
                value = UniversalDataOperation().get_dicts_value_by_key_path(global_dict["data_current"]["resp"], key)
            elif key_type == "LRESPONSE":
                value = UniversalDataOperation().get_dicts_value_by_key_path(global_dict["data_last"]["resp"], key)
            else:
                value = UniversalDataOperation().get_dicts_value_by_key_path(global_dict, key)
            return value
        except KeyError:
            raise Exception("键名异常: %s" % key)


# if __name__ == '__main__':
#     key_global = KeyGlobal()
#     parser_global = KeyGlobal()
#     parser_global.set_global_key('age', '36')
#     key_global.set_global_key('name', 'jack')
#     print(key_global.get_global_key('age'))
