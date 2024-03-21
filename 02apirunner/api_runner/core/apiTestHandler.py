# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     apiTestHandler.py
# Author:      Jakilo
# Datetime:    2024/1/22 17:00
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

import jsonpath
import json

from requests import Response, request, session

from api_runner.utils.log import Log


class ApiTestHandler:
    """
    ApiTest的核心执行器，包括请求逻辑、断言逻辑、抽取逻辑
    """

    def __init__(self, config: dict, log: Log):
        self.config = config
        self.log = log

    def request_method(self, request_content: dict) -> Response:
        if self.config:
            self.log.info(f'config:{self.config}')
        proxy = {"http": "127.0.0.1:8888"}
        self.log.info(f'request_content:{request_content}')
        resp = request(**request_content,proxies=proxy)
        self.log.info(f'request_content:{resp}')
        return resp

    def assert_method(self, assert_option: dict, resp: Response) -> None:
        self.log.info(f'assert_option:{assert_option}')
        pass

    def extract_method(self, extract_content: dict, context):
        self.log.info(f'extract_content:{extract_content}')
        pass
