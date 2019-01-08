#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "yong.guo"
from utils.logger.Log import Log


class UniversalDataOperation(object):
    def __init__(self):
        self.iterative_values = False
        self.L = Log("KeyGeneralMethods").logger

    def get_dicts_value_by_key_path(self, dicts: dict, key_path: str) -> str or list:
        """
        字典路径下的数据获取
        :param dicts: 需要解析的源数据
        :param key_path: 解析的路径，用"."号隔开，如：content.pn
        :return: 返回解析结果
        :return: str or list
        """
        # 将传入的字符串格式化为list
        key_path_r = key_path.split(".")

        # 调用私有方法进行解析
        self.iterative_values = "__iterations__" in key_path_r
        result = self.__get_dicts_value_by_key_path(dicts, key_path_r)

        # 若返回到是字符串直接返回，若返回的是list且是一个元素返回字符串，若返回的是list且是多个元素返回一维list
        if isinstance(result, list):
            if len(result) == 1:
                self.L.debug("通过路径%s,查找到的数据是%s" % (key_path, result[0]))
                return result[0]
            else:
                self.L.debug("通过路径%s,查找到的数据是%s" % (key_path, result))
                return result
        else:
            self.L.debug("通过路径%s,查找到的数据是%s" % (key_path, result))
            return result

    def __get_dicts_value_by_key_path(self, dicts: dict or list, key_path: list) -> str or list:
        """
        实现字典值索引
        :param dicts: 需要解析的源数据
        :param key_path: 解析的路径，按list形式传入
        :return: 返回解析结果
        """

        try:
            # 获取传入的字符串中的第一个key,
            i = key_path[0]

            # 判断当前是否为查找路径终点，若为终点，则直接取之返回。 否则继续往后查找字符串
            if len(key_path) > 1:
                # 若查找的路径不是叶子节点，则删除当前节点
                del key_path[key_path.index(i)]

                # 传入的参数是关键字"__iterations__"时，直接使用当前传入的字典
                if "__iterations__" == i:
                    return self.__get_dicts_value_by_key_path(dicts, key_path)

                # 传入的参数是数字时，从当前路径中，取出指定id下的值
                elif i.isdigit():
                    return self.__get_dicts_value_by_key_path(dicts[int(i)], key_path)

                # 当传入的是一个字符串时，取出对应key下的value
                else:

                    # 取值时，若是在list中，需要到list中去取对应key的值
                    if isinstance(dicts, list):
                        temp_list = []
                        for x in dicts:
                            temp_list.append(x[i])
                        return self.__get_dicts_value_by_key_path(temp_list, key_path)

                    # 取值时，若是在dict中，直接取对应key的值
                    else:
                        return self.__get_dicts_value_by_key_path(dicts[i], key_path)

            # 判断当前查找是否为叶子节点，并返回最终叶子节点值
            else:

                # 叶子节点传入的参数是关键字"__iterations__"时，直接使用当前传入的字典
                if "__iterations__" == i:

                    # 叶子节点
                    if isinstance(dicts, list):
                        return self.__list_flatten(dicts)
                    else:
                        return dicts
                        # return dicts[i]

                # 叶子节点传入的参数是数字时，返回指定节点值
                elif i.isdigit():

                    # 在叶子节点前，若出现过关键字"__iterations__"时，是返回每个节点下的第一个值
                    if self.iterative_values:
                        tmp = []
                        for x in dicts:

                            # 检查传入的值是否超过list下标，若超过不做处理
                            if len(x) > int(i):

                                # 若传入的是list,直接取出对应id的值
                                if isinstance(x, list):
                                    tmp.append(x[int(i)])

                                # 若传入的是字符串，直接取出对应的值
                                else:
                                    tmp.append(x)
                        return tmp

                    # 在叶子节点前，若没出现过关键字"__iterations__"时，直接返回指定的值
                    else:
                        return dicts[int(i)]

                # 叶子节点传入的参数是字符串时，返回指定节点值
                else:

                    # 取值时，若是在list中，需要到list中去取对应key的值
                    if isinstance(dicts, list):
                        temp_list = []
                        for x in dicts:
                            temp_list.append(x[i])
                        return temp_list

                    # 取值时，若是在字典中，直接取出对应值
                    else:
                        return dicts[i]

        except Exception as e:
            raise Exception("\n在内存数据:\n%s中\n未找到键:%s\nKeyError：%s" % (dicts, key_path, e))

    def __list_flatten(self, list_src: list) -> list:
        """
        用于多层嵌套list解包，还原到1层list
        :param list_src:
        :return:
        """
        tmp = []
        for i in list_src:
            if type(i) is not list:
                tmp.append(i)
            else:
                tmp.extend(self.__list_flatten(i))
        return tmp
