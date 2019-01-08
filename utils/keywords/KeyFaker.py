#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "xiujuan.chen"
from utils.logger.Log import Log
from faker import Factory
import random


class KeyFaker(object):
    """
    按指定条件生成随机数据
    """
    def __init__(self):
        self.L = Log("KeyFaker").logger

    def get_some_things(self, faker_type: str = "" or list) -> str or int or float:
        """
        根据faker type生成响应数据，并返回结果
        :param faker_type: mobile, farm, name, shop, int, float
        :return:
        """
        data = ""
        fake = Factory().create('zh_CN')
        # 传入为list时,随机返回list中的一个值
        if isinstance(faker_type, list):
            return random.choice(faker_type)
        elif isinstance(faker_type, str):
            # 若传入时下列关键字,返回对应的值
            record = faker_type.lower()

            if record == 'mobile':
                data = fake.phone_number()
                self.L.info("随机生成手机号:%s" % data)

            elif record == 'farm':
                data = fake.company_prefix() + "的" + fake.name() + "在中国" + fake.city() + "的农场"
                self.L.info("随机生成农场名:%s" % data)

            elif record == 'name':
                data = fake.name()
                self.L.info("随机生成用户民:%s" % data)

            elif record == 'shop':
                data = fake.company()
                self.L.info("随机生成店铺名:%s" % data)

            elif record == 'integer':
                data = random.randint(1, 100)
                self.L.info("随机生成整数:%s" % data)

            elif record == 'decimal':
                data = random.uniform(1, 50)
                self.L.info("随机生成小数:%s" % data)
            elif record == 'text':
                data = (fake.text().replace("\n", " "))[:20]
                self.L.info("随机20位字符串:%s" % data)
            elif record == 'address':
                data = fake.address()
                self.L.info("随机生成地址:%s" % data)
        else:
            data = faker_type
        return data

# if __name__ == '__main__':
#         f = KeyFaker()
#         f.get_some_things('farm')