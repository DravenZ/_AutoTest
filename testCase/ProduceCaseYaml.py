#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__ = 'Heng Xin'
__date__ = '2018/12/22'
"""

import os
import json
import codecs
import time
from utils.logger.Log import Log
from utils.basic.SendRequest import SendRequest
import yaml

# 暂时通过新建的service-config.yaml读取服务配置, 待郭老师规范
hosts = yaml.load(open("./service-config.yaml", encoding='utf-8'))['HOSTS']['DEV_HOST']


class ProduceCaseYaml(object):
    """
    根据服务配置, 自动生在/testCase/templates下生成Case的Yaml模板
    """

    def __init__(self):
        self.L = Log("ProduceCaseYaml").logger

    def get_paths_yaml(self, file_name: str, host_name: str) -> None:
        """
        通过Swagger V2获取api文档
        :param file_name: 想要存储yaml模板文件的文件名
        :param host_name: 各服务域名
        :return: 获取文档方法无需返回
        """
        json_content = SendRequest().get(str(host_name) + '/v2/api-docs')
        # 获取所有的paths节点
        paths = json.loads(json_content)["paths"]
        path_detail_list = []
        for p in paths:
            para_desc_list = []
            try:
                desc = paths[p]["post"].get("tags", [])[0]
                para_desc_list.append(desc)
                # L.logger.debug("{'%s': '%s'}" % (p, desc))
                paras = paths[p]["post"].get("parameters", [])
            except KeyError:
                desc = paths[p]["get"].get("tags", [])[0]
                para_desc_list.append(desc)
                # L.logger.debug("{'%s': '%s'}" % (p, desc))
                paras = paths[p]["get"].get("parameters", [])
            p_dict = {}
            if paras is None:
                pass
            else:
                for para in paras:
                    p_dict[para['name']] = u"%s_%s_%s" % (para.get('type', 'noType'),
                                                          para.get('required', 'noRequired'),
                                                          para.get('description', 'noDescription'))
            para_desc_list.append(p_dict)
            path_detail_list.append({p: para_desc_list})
        # demand_list = sorted(path_detail_list)
        now = time.strftime("_%Y-%m-%d_%H%M%S", time.localtime())
        # L.logger.debug(path_detail_list)
        current_path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(current_path + "/templates"):
            os.makedirs(current_path + "/templates")
        with codecs.open('./templates/' + str(file_name) + now + '.yaml', 'a', 'utf-8') as f:
            for item in path_detail_list:
                for k, v in item.items():
                    if isinstance(v[1], dict):
                        f.write('\n%s:' % k)
                        f.write('''
    baseInfo:
        author:
        time: 20180931
        logInfo: Debug
        directExecution: True
        generatePython: False
        requestMethod: POST
        requestHeaders: {'Host':'www.super-ping.com','Connection':'keep-alive','Cache-Control':'max-age=0','Accept':'text/html,*/*;q=0.01','X-Requested-With':'XMLHttpRequest','User-Agent':'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/41.0.2272.89Safari/537.36','DNT':'1','Referer':'http://www.super-ping.com/?ping=www.google.com&locale=sc','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6'}
        serverAddress: %s
        dataBase:
            host: 39.104.28.40
            port: 3306
            user: root
            password: YYJNo$QsaaSjgb8U3JoigB
            database: %s
    interfaceParameters:
        -
    ''' % (host_name, file_name.replace("_", "-").lower()))
                        for x, y in v[1].items():
                            f.write('      %s:\n    ' % x)
                    f.write('interfaceAsserts:\n        -\n')

    def add_latest_yaml(self):
        for key, host in hosts.items():
            try:
                self.get_paths_yaml(key, host)
            except Exception as e:
                self.L.error("错误信息: %s" % e)


if __name__ == '__main__':
    pcy = ProduceCaseYaml()
    pcy.add_latest_yaml()
