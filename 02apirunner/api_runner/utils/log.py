# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     log.py
# Author:      Jakilo
# Datetime:    2024/1/18 14:02
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import os
import logging
from api_runner.utils.baseTools import SupportTest
from api_runner.utils.path import PathOperation


class Log:
    """
    生成日志类
    """
    def __init__(self, module, **kwargs):

        self.log_base = 'log'
        self.error_number = 0

        self.logdir = os.path.join(self.log_base, f'{SupportTest.current_time()[0]}')

        self.log_module_path = os.path.join(self.logdir, f'{module + "_" + SupportTest.current_time()[1]}.log')
        print(f'当前日志地址:{self.log_module_path}')
        self.current_log = PathOperation().make_dir_or_path(self.log_module_path)

    def __del__(self):
        if self.error_number:

            print(f'本次运行error数量{self.error_number}')

    def __print_console(self, level, message):
        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.current_log, 'a', encoding='utf8')
        fh.setLevel(logging.DEBUG)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        if level == 'info':

            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)

        # 记录完日志移除句柄Handler
        logger.removeHandler(ch)
        logger.removeHandler(fh)

        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__print_console('debug', message)

    def info(self, message):
        self.__print_console('info', message)

    def info2(self, message):
        self.__print_console('info', message)

    def warning(self, message):
        self.__print_console('warning', message)

    def error(self, message):
        self.error_number += 1
        self.__print_console('error', message)
