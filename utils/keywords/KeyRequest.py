#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "yong.guo"
from utils.logger.Log import Log
from utils.keywords.KeyGlobal import KeyGlobal


class KeyRequest(object):
    """
    1.解析data_file中关键字REQUEST、GREQUEST、LREQUEST、IMAGE的用法，并执行请求，将请求结果按str类型返回给调用方
    2.REQUEST() 关键字，返回当前请求中参数值，如REQUEST(id),则返回当次请求中id的值 在data_current中获取
    3.LREQUEST() 关键字，返回上一次请求中参数值，如LREQUEST(id),则返回上次请求中id的值 在data_last中获取
    4.IMAGE() 关键字，参数是图片路径，用户请求中，说明该接口参数是图片信息
    """

    def __init__(self):
        self.L = Log("KeyRquest").logger
        self.kg = KeyGlobal()

    def get_current_request_info_by_argument(self, field_name: str) -> str or dict or list:

        """
        解析关键字REQUEST()
        :param field_name: 当前请求中那个参数的值
        :return:
        """
        try:
            self.L.info("解析关键字REQUEST，解析路径为: %s" % field_name)
            result = self.kg.get_global_value_by_key(field_name, "REQUEST")
            self.L.debug("解析REQUEST(%s)的结果是：%s" % (field_name, result))
            return result
        except Exception as e:
            raise Exception("解析关键字REQUEST数据异常，异常信息：%s" % e)

    def get_last_request_info_by_argument(self, field_name: str) -> str or dict or list:
        """
        解析关键字LREQUEST()
        :param field_name: 上次请求中那个参数的值
        :return:
        """
        try:
            self.L.info("解析关键字LREQUEST，解析路径为: %s" % field_name)
            result = self.kg.get_global_value_by_key(field_name, "LREQUEST")
            self.L.debug("解析LREQUEST(%s)的结果是：%s" % (field_name, result))
            return result
        except Exception as e:
            raise Exception("解析关键字LREQUEST数据异常，异常信息：%s" % e)

    def get_image_info(self, image_name: str) -> str:
        """
        解析关键字IMAGE()
        :param image_name: 图片详细路径或名字
        :return:
        """
        try:
            return image_name
        except Exception as e:
            raise Exception("解析关键字IMAGE数据异常，异常信息：%s" % e)

    # def _parser_dicts(self, dicts: dict, key_path) -> str:
    #     """
    #     关键字结果解析（不支持list解析）
    #     :param dicts: 需要解析的源数据
    #     :param key_path: 解析的路径，用"."号隔开，如：content.datas
    #     :return: 返回解析结果
    #     """
    #     try:
    #         # 获取传入的字符串中的第一个key,
    #         i = key_path[0]
    #         # 判断当前是否为查找路径终点，若为终点，则直接取之返回。 否则继续往后查找字符串
    #         if len(key_path) > 1:
    #             # 若查找的路径不是叶子节点，则删除当前节点
    #             del key_path[key_path.index(i)]
    #             # 继续完后查找是否为叶子节点，并返回最终叶子节点值
    #             return self._parser_dicts(dicts[i], key_path)
    #         else:
    #             # 返回最终叶子节点值
    #             return dicts[i]
    #     except Exception as e:
    #         raise Exception("\n在字典:\n%s中\n未找到键:%s\nKeyError：%s" % (dicts, key_path, e))

# if __name__ == '__main__':
#     test = KeyRquest()
#     path1 = "province.__iterator__.cities.city.__iterator__"
#     path2 = "province.__iterator__.cities.city.12"
#     path = "province.0"
#     test.get_current_request_info_by_argument(path)
#     # test.get_last_request_info_by_argument("content.ps")
