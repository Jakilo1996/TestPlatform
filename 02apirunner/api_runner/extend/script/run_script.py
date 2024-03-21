# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     run_script.py
# Author:      Jakilo
# Datetime:    2024/1/18 15:29
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


def exec_script(script, step, context) -> None:
    """

    :param script:
    :param step:
    :param context:
    :return:
    """
    if script is None:
        return

    script = "from api_runner.extend.functions import * \n" + script
    # print(script)
    try:
        exec(script, {"step": step, "context": context})
    except Exception as e:
        e.args = ("Exception extend/run_script/exec_script :"+e.args[0],)
        raise e
    print(context)
