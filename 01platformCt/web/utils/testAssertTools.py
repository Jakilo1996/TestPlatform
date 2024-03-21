# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     testAssertTools.py
# Author:      Jakilo
# Datetime:    2024/3/15 16:24
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from typing import Callable, Type, List, Dict, Union
from functools import wraps

from jsonpath import jsonpath


class AssertHandler:
    @staticmethod
    def json_path_v2(object_: Type, expr: str) -> Union[List[Dict], Dict[str, str], str]:
        """
        :param object_: 一个待提取的json返回值；1：json字符串 response.json()返回值 2；被mysql类处理过的对象，期望是一个字典
        :param expr: 传入一个JsonPath表达式
        :return: 如果expr 无法提取出对应的value 则抛出ValueError；如果对应的object 不属于可以JsonPath的格式，则抛出ValueError
        如果expr 提取的值仅能返回一个数据，则返回数据 object，如果返回多组数据，则返回列表 list
        """
        reason = jsonpath(object_, expr)
        if not reason:
            raise ValueError(f'JsonPath 不能提取到结果,表达式:{expr},抽取对象{object_}')
        elif len(reason) == 1:
            return reason[0]
        else:
            return reason


# 声明一个报错处理装饰器，装饰一个类，指定一种报错类型，如果出现此类报错类型，则进行log打印
def assert_ec_decorator(error_msg_template: str, success_msg_template: str,
                        ec: Exception = AssertionError) -> Callable:
    """

    :param error_msg_template: 报错的模版：需要留下4个可format的位置
    :param success_msg_template: 成功的模版，需要留下两个可format的位置
    :param ec: 捕获函数执行的报错类型
    :return: assert_func
    """

    def inner(func: Callable):
        """
        :param func: 断言函数
        :return:
        """

        @wraps(func)
        def call(*args, **kwargs):
            log = kwargs.get('log')
            expected = kwargs.get('assert_option').get('expected')
            actual = kwargs.get('actual')
            if not log:
                raise ValueError('assert method has no log')
            try:
                func(*args, **kwargs)
            except ec:
                log.error(
                    f'AssertError {func.__name__} method '
                    f'{error_msg_template.format(expected, actual, expected, actual)}')
                raise
            except Exception as e:
                log.error(f'{func.__name__} method raise {e.__name__}')

                raise
            else:
                log.info(
                    f'AssertSuccess {func.__name__} ,{success_msg_template.format(expected, actual)}')

        return call

    return inner
