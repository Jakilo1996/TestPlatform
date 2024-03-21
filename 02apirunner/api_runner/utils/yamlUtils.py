# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     yamlController.py
# Author:      Jakilo
# Datetime:    2024/1/26 17:07
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

import yaml
from yamlinclude import YamlIncludeConstructor


def load_yaml(yaml_file_path):
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except Exception as e:
        print(f"装载yaml文件{yaml_file_path}错误: {str(e)}")
        raise e


if __name__ == '__main__':
    from pprint import pprint
    pprint(load_yaml('/Users/qiujie/study/my_code/platform/02apirunner/examples/suit_debug_yaml_1/0_testLogin.yaml'))