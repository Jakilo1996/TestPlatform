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


# from yamlinclude import YamlIncludeConstructor

class YamlHandler:
    @staticmethod
    def load_yaml(yaml_file_path):
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as file:
                return yaml.load(file, Loader=yaml.FullLoader)
        except Exception as e:
            print(f"装载yaml文件{yaml_file_path}错误: {str(e)}")
            raise e

    @staticmethod
    def dump_yaml(_data, _file):
        yaml.dump(_data, _file, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    @staticmethod
    def write_yaml_file(file_path: str, file_data: dict):
        with open(file_path, "w", encoding="utf-8") as fp:
            YamlHandler.dump_yaml(file_data, fp)


if __name__ == '__main__':
    from pprint import pprint

    YamlHandler.write_yaml_file(
        r'~/work/test_platform/debug_case/f5f26a28-699e-45fb-b1a9-7819b573b9f9/1_101ab5dd-cc49-4134-a562-a6f3bf3fda8c.yamltest_case_yaml_file',
        {'desc': '测试百度', 'steps': [{'url': 'www.baidu.com', 'method': 'GET'}]})
    # pprint(load_yaml('/Users/qiujie/study/my_code/platform/02apirunner/examples/suit_debug_yaml_1/0_testLogin.yaml'))
