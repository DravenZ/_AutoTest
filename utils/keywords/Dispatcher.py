#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "xin.heng@worldfarm.com"


from utils.keywords.KeyFaker import KeyFaker
from utils.keywords.KeyGlobal import KeyGlobal
# from utils.keywords.KeyReckon import *
# from utils.keywords.KeyRegex import *
from utils.keywords.KeyRequest import KeyRequest
from utils.keywords.KeyResponse import KeyResponse
from utils.keywords.KeySquery import KeySquery
# from utils.keywords.KeySuper import *
from utils.logger.Log import Log


class Dispatcher(object):
    def __init__(self):
        """
        解析参数中的key或value信息，并返回各自关键字执行结果
        """
        self.L = Log("Dispatcher").logger

    def key_dispatcher(self, t_key_string: object, record_value="") -> object:
        """
        此为本类函数入口点, 将入参字符串转为 元组 待递归解析
        :param t_key_string: 解析由Runner.py传入的字符串
        :param record_value: 默认为空, 仅适用于RECORD关键字字典存值使用
        :return: 返回 递归解析并调用路由后 的结果字符串
        """
        if isinstance(t_key_string, str) is False:
            return t_key_string
        else:
            return self.__key_dispatcher_realize((t_key_string, ), record_value)

    def __key_dispatcher_realize(self, t_key: tuple, record_value: str = "") -> str:
        """
        解析由key_dispatcher传入的 (待解析字符串, ) 元组, 递归解析字符串路中的关键字,
        路由匹配调用各关键字类(如: KeyRequest, KeySquery)返回调用后结果字符串
        :param t_key: 由runner调用时传入的字符串key转为的(key, )元组
        :param record_value: 默认为空, 仅适用于RECORD关键字字典存值使用
        :return: 若还可递归, 继续以 (递归函数本身, 关键字, 参数) 的元组 为入参 调用函数本身; 若无法递归 则返回字符串
        """
        # 所有传入字符串 以 左括号 做字符串切片 以解析 关键字 和 入参
        if t_key[0].find('(') == -1:
            # 最后的字符串已不包含左括号
            return t_key[0]
        else:
            # 以第一个左括号位置切片 解析 关键字 和 入参
            left_str = (t_key[0][:t_key[0].find('(')])
            # 去掉 待解析字符串中的 首尾括号; 否则 下次左括号位置为0时, 会导致解析错误
            right_str = (t_key[0][t_key[0].find('(')+1:-1])
            self.L.info("关键字: %s; 参数: %s" % (left_str, right_str))
            return self.__key_route((left_str, self.__key_dispatcher_realize((right_str, left_str))), record_value)

    def __key_mapper(self, check_str: str, except_key: str) -> bool:
        """
        解析由递归函数传入字符串check_str中是否含有期望的关键字except_key, 如REQUEST, LREQUEST, RESPONSE等
        :param check_str: 由递归函数传入字符串
        :param except_key: 期望的关键字except_key, 如REQUEST, LREQUEST, RESPONSE等
        :return: 匹配则返回True, 反之则反
        """
        result = check_str.split(" ")[-1:][0] == except_key
        self.L.debug("%s == %s -> %s" % (check_str, except_key, result))
        return result

    def __key_route(self, key_tuple: tuple, record_value: str = "") -> str:
        """
        解析由key_dispatcher函数传入的(key_dispatcher对象, 关键字, 参数)的元组,
        匹配调用各关键字类(如: Request(content.id))返回调用各关键字类的结果字符串
        :param key_tuple: 由key_dispatcher函数传入的(key_dispatcher对象, 关键字, 参数)的元组
        :param record_value: 默认为空, 仅适用于RECORD关键字字典存值使用
        :return: 调用各关键字类的结果字符串
        """
        # todo: 仅与KeyRequest完成联调, 其他类待联调. 递归最后一层不出日志(情况未知), 尚无其他副作用
        self.L.debug("left: %s | right: %s" % (key_tuple[0], key_tuple[1]))
        if self.__key_mapper(key_tuple[0], "REQUEST"):
            self.L.info("REQUEST is CALLED")
            kr = KeyRequest()
            return kr.get_current_request_info_by_argument(key_tuple[1])
        elif self.__key_mapper(key_tuple[0], "LREQUEST"):
            self.L.info("LREQUEST is CALLED")
            kr = KeyRequest()
            return kr.get_last_request_info_by_argument(key_tuple[1])
        elif self.__key_mapper(key_tuple[0], "RESPONSE"):
            self.L.info("RESPONSE is CALLED")
            kres = KeyResponse()
            return kres.get_current_response_message(key_tuple[1])
        elif self.__key_mapper(key_tuple[0], "LRESPONSE"):
            self.L.info("LRESPONSE is CALLED")
            kres = KeyResponse()
            return kres.get_last_response_message(key_tuple[1])
        elif self.__key_mapper(key_tuple[0], "RECORD"):
            self.L.info("RECORD is CALLED")
            kg = KeyGlobal()
            return kg.set_global_key(key_tuple[1], record_value)
        elif self.__key_mapper(key_tuple[0], "READ"):
            self.L.info("READ is CALLED")
            kg = KeyGlobal()
            return kg.get_global_value_by_key(key_tuple[1])
        elif self.__key_mapper(key_tuple[0], "SQUERY"):
            self.L.info("SQUERY is CALLED")
            sq = KeySquery()
            return sq.get_sql_result(key_tuple[1])
        elif self.__key_mapper(key_tuple[0], "FAKER"):
            self.L.info("FAKER is CALLED")
            kf = KeyFaker()
            return kf.get_some_things(key_tuple[1])
        elif self.__key_mapper(key_tuple[0], "REGEX"):
            self.L.info("REGEX is CALLED")
            # return "REGEX"
        else:
            raise Exception('非法关键字: %s'
                            '\n合法的关键字:'
                            '\nREQUEST 用于立即发送网络请求, '
                            '\nLREQUEST 用于获取上次请求, '
                            '\nRESPONSE 用于立即获取网络响应, '
                            '\nLRESPONSE 用于获取上次网络响应, '
                            '\nSQUERY 用于查询数据库, '
                            '\nRECORD 用于存储全局缓存, '
                            '\nREAD 用于读取全局缓存, '
                            '\nFAKER 用于伪造数据, '
                            '\nREGEX 用于正则校验'
                            '' % str(key_tuple[0]))


# if __name__ == '__main__':
#     import yaml
#     import json
#     yaml_data = yaml.load(open("./../../testCase/yaml-demo-instance.yaml", encoding='utf-8'))
#     json_data = json.dumps(yaml_data)
#     input_param = yaml_data["/api/sso/login"]["interfaceParameters"][1]["code2"]
#     print(input_param)
#     dispatcher = Dispatcher()
#     dispatcher.key_dispatcher(input_param)
