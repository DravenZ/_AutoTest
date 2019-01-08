#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = ""
from utils.logger.Log import Log
from utils.keywords.KeyGlobal import KeyGlobal
import pymysql


class KeySquery(object):
    """
    SQUERY(sql) 执行sql，将数据结果以list形式返回,如果list长度只有一个，则直接返回值
    """
    def __init__(self):
        self.L = Log("KeySquery").logger

    def get_sql_result(self, sql: str)-> str or list or int or float:
        """
        SQUERY(sql) 执行sql，将数据结果以list形式返回,若只有一个元素则直接返回一个元素
        :param sql:
        :return:
        """
        try:
            # 执行SQL
            self.L.info("准备执行SQL：%s" % sql)
            cursor = self.__connect_database().cursor()
            cursor.execute(sql)
            result_tmp = cursor.fetchall()
            self.L.info("SQL执行结果 %s" % result_tmp)

            # 将返回的SQL结果序列成一维list
            result = []
            for x in result_tmp:
                for y in list(x.values()):
                    result.append(y)

            # 多个数据结果以list形式返回,一个元素则直接返回一个元素
            if len(result) < 2:
                return result[0]
            else:
                return result
        except Exception as e:
            raise Exception("执行SQL异常 %s" % e)

    def __connect_database(self):
        """
         链接数据库
        """
        try:
            kg = KeyGlobal()
            config = kg.get_global_value_by_key("baseInfo.dataBase")
            self.L.debug("host: %s, database: %s" % (config["host"], config["database"]))
            db = pymysql.connect(host=config["host"], user=config["user"], port=config["port"],
                                 password=config["password"], database=config["database"],
                                 cursorclass=pymysql.cursors.DictCursor)
            return db
        except ConnectionError as e:
            raise ConnectionError("连接数据库错误 %s" % e)
