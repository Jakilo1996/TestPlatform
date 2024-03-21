# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     varRender.py
# Author:      Jakilo
# Datetime:    2024/1/22 10:42
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:  字符串模板渲染
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from typing import Union
from jinja2 import Template


def refresh_var(var_target: Union[str, dict], g_context: dict) -> Union[None, str]:
    """
    变量渲染操作
    :param var_target: 渲染的目标
    :param g_context: 渲染对应的上下文
    :return: None，或者渲染后的变量
    """
    if var_target:
        return Template(str(var_target)).render(g_context)
    else:
        return None


if __name__ == '__main__':
    # 单元测试
    target = "hello {{name}}, {{niasd}}"
    context = {"name": "张三"}
    print(refresh_var(target, context))
