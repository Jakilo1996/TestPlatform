# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     jsonUtils.py
# Author:      Jakilo
# Datetime:    2024/1/26 17:28
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

import json
from typing import Any

from common.lib.funcBase import BaseTools


class JsonHandler:
    @staticmethod
    def load_json(json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"装载json文件{json_file_path}错误: {str(e)}")
            raise e

    @staticmethod
    def loads_json(loads_str):
        return json.loads(loads_str)

    @staticmethod
    def eval_str_to_json(data: Any) -> str:
        """
        传入任何格式，如果是一个可以转义为python类型的字符串，将其序列化成json字符串，如果已经是字典或列表，则直接序列化成json
        :param data:
        :return:
        """
        if isinstance(data, str):
            return json.dumps(BaseTools.eval_str(data))
        elif isinstance(data, (dict, list)):
            return json.dumps(data)


if __name__ == '__main__':
    from pprint import pprint

    pprint(JsonHandler.load_json(
        '/Users/qiujie/study/my_code/platform/02apirunner/examples/suit_debug_json_2/0_testLogin.json'))
