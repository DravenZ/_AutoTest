#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "yong.guo"
from resolver.runner.Runner import Runner
from utils.logger.Log import Log
import unittest
import os.path


class TestMain(unittest.TestCase):
    def setUp(self):
        """
        测试用例前置条件
        :return:
        """
        self.L = Log("MyTestClass").logger
        self.L.critical("测试准备")
        self.runner = Runner()
        self.case_path = os.path.abspath(".")+"/testCase/"

    def test_user_login(self):
        """
        测试用户登录
        :return:
        """
        case_path = self.case_path+"user.yaml"
        self.L.info("开始执行测试用例：%s" % case_path)
        self.runner.do_request(case_path)

    def test_user_logout(self):
        """
        测试用户注销
        :return:
        """
        case_path = self.case_path+"user.yaml"
        self.L.info("开始执行测试用例：%s" % case_path)
        self.runner.do_request(case_path)

    def test_customer(self):
        """
        测试苗叔向基地购买流程
        :return:
        """
        case_path = self.case_path+"苗叔向基地购买流程.yaml"
        self.L.info("开始执行测试用例：%s" % case_path)
        self.runner.do_request(case_path)

    def test_user_shop(self):
        """
        测试基地库存
        :return:
        """
        case_path = self.case_path+"Shopbuy.yaml"
        self.L.info("开始执行测试用例：%s" % case_path)
        self.runner.do_request(case_path)
