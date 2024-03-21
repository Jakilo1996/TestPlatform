# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     cli.py
# Author:      Jakilo
# Datetime:    2024/1/18 11:43
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:  工具入口
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

import argparse
import pytest

from api_runner.core.testCasesPlugin import TestCasesPlugin
from api_runner.utils.path import PathOperation


def split_pytest_args(pytest_args_str: str) -> list:
    """
    # 声明一个方法，用于处理命令行中 支持pytest自带参数
    :param pytest_args_str:
    :return: test_args_list
    """
    return [i for i in pytest_args_str.replace('_', '-').split(',')]


def run() -> None:
    """
    主函数入口
    :return:
    """
    po = PathOperation()
    parser = argparse.ArgumentParser(description='ApiAutoTest')
    parser.add_argument('--case_path', type=str, default='', help='mode2和mode3 需要传入此参数，指定测试用例的文件或者目录')
    parser.add_argument('--pytest_args', type=str, help='支持的pytest命令行参数，用,分割每个参数')
    parser.add_argument('-v', action='store_true', help='-v : 打印版本信息')
    args = parser.parse_args()
    print(f'命令行参数收集完成：{vars(args)}')
    _pytest_args = ["-s", "-v", "--capture=sys",
                    po.proj_path_join('api_runner/core', "testRunner.py"),
                    "--type=yaml",
                    f"--cases={args.case_path}"]
    if args.pytest_args:
        _pytest_args += split_pytest_args(args.pytest_args)
    print(_pytest_args)
    pytest.main(_pytest_args, plugins=[TestCasesPlugin()])


if __name__ == '__main__':
    run()
    pass
    # print(__name__, __package__)
    # po = PathOperation()
    # pytest_args = ["-s", "-v", "--capture=sys",
    #                po.proj_path_join('api_runner/core', "testRunner.py"),
    #                "--clean-alluredir",
    #                "--alluredir=allure-results",
    #                "--type=yaml",
    #                "--cases=examples/suit_debug_yaml_1"]
    # # pytest.main(pytest_args, plugins=[TestCasesPlugin()])
    # # pytest_args = ["-s", "-v", "--capture=sys",
    # #                po.proj_path_join('api_runner/core', "testRunner.py"),
    # #                "--clean-alluredir",
    # #                "--alluredir=allure-results",
    # #                "--type=json",
    # #                "--cases=examples/suit_debug_json_2"]
    # pytest.main(pytest_args, plugins=[TestCasesPlugin()])
