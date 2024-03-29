# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     logUtil.py
# Author:      Jakilo
# Datetime:    2024/3/14 21:27
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -------------------------------------------------------------------Ò----------------

import logging
from app import application

from common.lib.timeBase import TimeBase
from common.lib.pathBase import PathOperation
from common.lib.logBase import LogBase, make_log_handler

# 获取配置中指定的相关日志文件地址
PLATFORM_PROCESS_LOG_TAG = application.config['PLATFORM_PROCESS_LOG_TAG']
PLATFORM_PROCESS_LOG = application.config['API_CASES_ROOT_DIR']
platform_process_log = False
PLATFORM_USER_LOG_TAG = application.config['PLATFORM_USER_LOG_TAG']
PLATFORM_USER_LOG = application.config['PLATFORM_USER_LOG']
platform_user_log = False
PLATFORM_RUN_COLLECTION_LOG_TAG = application.config['PLATFORM_RUN_COLLECTION_LOG_TAG']
PLATFORM_RUN_COLLECTION_LOG = application.config['PLATFORM_RUN_COLLECTION_LOG']
platform_run_collection_log = False
API_TEST_TOOLS_LOG_TAG = application.config['API_TEST_TOOLS_LOG_TAG']
API_TEST_TOOLS_LOG = application.config['API_TEST_TOOLS_LOG']
api_test_tools_log = False
PLATFORM_PROCESS_ACCESS_LOG_TAG = application.config['PLATFORM_PROCESS_ACCESS_LOG_TAG']
PLATFORM_PROCESS_ACCESS_LOG: str = application.config['PLATFORM_PROCESS_ACCESS_LOG']
platform_process_access_log = False

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
"""


# run_collection log  由平台生成并读取
# debug_test_case log  由平台生成并读取
# platform_process log  由平台生成，记录平台的运行记录

class LogOption:
    platform_process_log = False
    platform_user_log = False
    platform_run_collection_log = False
    api_test_tools_log = False
    if PLATFORM_PROCESS_LOG_TAG:
        platform_process_log = LogBase(PLATFORM_PROCESS_LOG)
    if PLATFORM_USER_LOG_TAG:
        platform_user_log = LogBase(PLATFORM_USER_LOG)
    if PLATFORM_RUN_COLLECTION_LOG_TAG:
        platform_run_collection_log = LogBase(PLATFORM_RUN_COLLECTION_LOG)
    if API_TEST_TOOLS_LOG_TAG:
        api_test_tools_log = LogBase(API_TEST_TOOLS_LOG)


def read_run_test_log():
    # run_test_tools log  由 testTools负责生成日志,平台提供 API 读取，本地日志
    pass


def platform_user_log():
    # flask 用户接口调用日志，调用装饰器需要返回成功，或者失败
    pass


def create_platform_process_access_log():
    # flask log 平台内部的运行接口访问日志
    application.logger.setLevel(logging.INFO)
    log_format = '%(asctime)s - %(remote_addr)s - %(request_method)s - %(request_path)s - %(status_code)s'
    PathOperation.make_dir_or_file(PLATFORM_PROCESS_ACCESS_LOG)
    # 创建一个日志处理程序，将访问日志记录到指定的文件中
    access_log_handler = make_log_handler(PLATFORM_PROCESS_ACCESS_LOG, formatter=log_format)
    # 将处理程序添加到 Flask 应用中
    application.logger.addHandler(access_log_handler)
    return access_log_handler


def create_platform_process_error_log():
    # flask log 平台内部的运行报错处理，记录平台的内部报错，处理内部的接口错误
    # DEBUG 模式下，需要打印所有接口的入参出参，TEST 模式下，仅打印错误
    pass


def test_result_log_analysis():
    # 分析完整运行的测试套件的日志运行结果，读取日志内容，  TestRunTools 需要修改 pytest 的钩子函数，完成日志写入格式的重新封装
    pass


def clean_log_crontab():
    # 定时清理过期的日志
    pass


# 比较日期并删除早于目标日期的文件
def delete_old_logs(log_folder, target_date):
    for file_path in PathOperation.traverse_folder(log_folder):
        file_date = TimeBase.extract_str_date(file_path)
        if file_date < target_date:
            # rm_dir(file_date)
            print(f"Deleted file: {file_path}")


def clean_log(log_folder: str):
    # 清理日志的主函数
    current_date = TimeBase.get_current_date()
    target_date = TimeBase.calculate_target_date(current_date)
    target_folder_path = PathOperation.build_target_folder_path(target_date)

    # 删除早于目标日期的日志文件
    delete_old_logs(log_folder, target_date)


if __name__ == '__main__':
    clean_log()
