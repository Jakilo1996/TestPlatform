# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     logBase.py
# Author:      Jakilo
# Datetime:    2024/3/15 23:32
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

import logging


def make_log_handler(file_handler, formatter='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    """
    返回日志句柄
    """
    _log_handler = logging.FileHandler(file_handler)
    _formatter = logging.Formatter(formatter)
    _log_handler.setFormatter(_formatter)


class LogBase:
    """
    TODO 方法需要重写，没有返回 log_Handler
    """

    def __init__(self, log_path):
        self.log_path = log_path

    def __print_console(self, level, message):
        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.log_path, 'a', encoding='utf8')
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
        self.__print_console('error', message)
