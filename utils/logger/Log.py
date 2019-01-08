#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
__author__ = "yong.guo"
import logging
import logging.config
from os import path


class Log(object):
    def __init__(self, log_name):
        log_file_path = path.join(path.dirname(path.abspath(__file__)), './logger.conf')
        logging.config.fileConfig(log_file_path)
        # logging.config.fileConfig('./logger.conf')
        self.logger = logging.getLogger(log_name)
