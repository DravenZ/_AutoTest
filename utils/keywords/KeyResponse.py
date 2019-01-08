#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "Baiying"
from utils.logger.Log import Log
from utils.keywords.KeyGlobal import KeyGlobal


class KeyResponse(object):
    """
    RESPONSE(路径) 读取响应数据data_current 中的RESPONSE值字段，并将值取出返回str
    LRESPONSE() 关键字，返回上一次请求data_last中参数值str，如LREQUEST(id),则返回上次请求中id的值
    特殊的，当入参中包含迭代器时，需要迭代查询结果，并按list形式返回，迭代标识符为 __iterations__  ,如传入的参数为key[__iterations__]["status"],返回key下每个模块中的status
    """
    def __init__(self):
        self.L = Log("KeyResponse").logger
        self.li = []
        self.kg = KeyGlobal()

        # self.global_data = json.loads('{"name":"中国","province":[{"name":"黑龙江","cities":{"city":["哈尔滨","大庆"]}},{"name":"广东","cities":{"city":["广州","深圳","珠海"]}},{"name":"台湾","cities":{"city":["台北","高雄"]}},{"name":"新疆","cities":{"city":["乌鲁木齐"]}}]}')

    def get_current_response_message(self, field_name: str) -> str or dict or list:
        """
        解析关键字RESPONSE()
        :param field_name: 当前请求中那个参数的值
        :return:
        """
        try:
            self.L.info("解析关键字RESPONSE，解析路径为: %s" % field_name)
            result = self.kg.get_global_value_by_key(field_name, "RESPONSE")
            self.L.debug("解析RESPONSE(%s)的结果是：%s" % (field_name, self.li))
            return result
        except Exception as e:
            raise Exception("解析关键字RESPONSE数据异常，异常信息：%s" % e)

    def get_last_response_message(self, field_name: str) -> str or dict or list:
        """
        解析关键字LRESPONSE()
         LRESPONSE() 返回接口响应中的，key(json中的数据路径)，下的数据
        """
        try:
            self.L.info("解析关键字LRESPONSE，解析路径为: %s" % field_name)
            result = self.kg.get_global_value_by_key(field_name, "LRESPONSE")
            self.L.debug("解析LRESPONSE(%s)的结果是：%s" % (field_name, self.li))
            print(result)
        except Exception as e:
            raise Exception("解析关键字LRESPONSE数据异常，异常信息：%s" % e)

    # def _parser_dicts(self, dicts, key_path):
    #     try:
    #         # 获取传入的字符串中的第一个key,
    #         i = key_path[0]
    #         # 判断当前是否为查找路径终点，若为终点，则直接取之返回。 否则继续往后查找字符串
    #         if key_path[0] == '__iterations__' and isinstance(dicts, list):
    #             key_path.pop(0)
    #             for j in range(len(dicts)):
    #                 if len(key_path) > 0:
    #                     # 继续完后查找是否为叶子节点，并返回最终叶子节点值
    #                     self._parser_dicts(dicts[j], key_path)
    #                 else:
    #                     # 返回最终叶子节点值
    #                     self.li.append(dicts[j])
    #         elif key_path[0].isdigit() is True:
    #             s = int(key_path[0])
    #             if len(key_path) > 1:
    #                 key_path.pop(0)
    #                 # 继续完后查找是否为叶子节点，并返回最终叶子节点值
    #                 self._parser_dicts(dicts[s], key_path)
    #             else:
    #                 # 返回最终叶子节点值
    #                 self.li.append(dicts[s])
    #         else:
    #             if len(key_path) > 1:
    #                 # 若查找的路径不是叶子节点，则删除当前节点
    #                 key_path1 = key_path.copy()
    #                 key_path1.pop(0)
    #                 # 继续完后查找是否为叶子节点，并返回最终叶子节点值
    #                 self._parser_dicts(dicts[i], key_path1)
    #             else:
    #                 # 返回最终叶子节点值
    #                 self.li.append(dicts[i])
    #
    #     except Exception as e:
    #         raise Exception("\n在字典:\n%s中\n未找到键:%s\nKeyError：%s" % (dicts, key_path, e))



# if __name__ == '__main__':
#     kr = KeyResponse()
#     # separator = '"" '
#     # d = {'name': 123, 'aaa': [{"name": 333}, {"name": 444}, {"name": 555}]}
#     # kr._parser_dicts(d, ['aaa', '__iterations__', 'name'])
#     # print(kr.li)
#     path1 = "province.__iterations__.cities.city.__iterations__"
#     path2 = "province.__iterations__.cities.city.1"
#     path = "province.__iterations__"
#     path4 = "province.__iterations__.cities"
#     path3 = ""
#     kr.get_current_response_message(path4)
#     # kr.get_last_response_message("content.ps")

