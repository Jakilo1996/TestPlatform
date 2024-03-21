# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     exceptionHandler.py
# Author:      Jakilo
# Datetime:    2024/3/14 21:08
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from common.lib.funcBase import ExceptionBase


def run_test_process_exception():
    # run_case_collection的装饰器，需要将这个函数中的报错都抛出，并记录运行日志 PLATFORM_RUN_COLLECTION_LOG
    # 运行 test 流程 的装饰器，将运行器内部的报错捕获并报错，
    # TODO
    """ catch_exceptions_callback
    需要做的事情，封装TestRun 的函数，捕获函数内的报错，并输出到对应日志，
    TODO 报错的结果返回到 web 吗
    QUESTION： 分析什么样的报错需要返回给执行端 web，作为 runCollection result ，什么样的日志需要作为系统的运行日志存储
    如何关联日志模块逻辑，那些日志是用户需要知道的运行日志，哪些日志需要系统本地存储
    Answer：
        测试运行相关的日志需要用户知道，并进行返回；
        测试平台执行了哪些测试套件，apiInfo 的变更信息，用户变更信息，数据的创建等
            需要进行记录，保存在系统日志中
        flask 内部的报错日志，需要持久化在本地，帮助进行 debug
    :param func:
    :return:
    """
    pass


def flask_process_exception():
    # 处理 flask 平台内部报错（API等），需要是个装饰器，装饰一些核心执行逻辑，并记录日志 PLATFORM_PROCESS_LOG
    pass


def test_platform_process_exception():
    # 处理API 等的参数错误等报错
    pass
