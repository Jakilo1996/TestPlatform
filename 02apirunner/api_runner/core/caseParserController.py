# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     caseParserController.py
# Author:      Jakilo
# Datetime:    2024/1/18 14:28
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:  用例解析器地址，根据不同的解析参数，解析不同的请求
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import copy
import os
from typing import Dict, Union, List

from api_runner.core.globalContext import GContext
from api_runner.utils.path import PathOperation
from api_runner.utils.yamlUtils import load_yaml
from api_runner.utils.jsonUtils import load_json
from api_runner.utils.log import Log


class CaseParser:
    def __init__(self, case_type: str, case_dir: str, log: Log):
        """

        :param case_type: 文件夹中文件的类型
        :param case_dir: 文件夹的父目录路径
        """
        self.case_type = case_type
        self.case_dir = case_dir
        self.log = log
        self.po = PathOperation()

    def load_context_from_type(self) -> bool:
        """
        将指定 suit 下的 context 读出来渲染到 context 中
        :return:
        """
        try:
            context_data = {}
            file_path = os.path.join(self.case_dir, f'context.{self.case_type}')
            if self.case_type == 'yaml':
                context_data = load_yaml(file_path)

            elif self.case_type == 'json':
                context_data = load_json(file_path)
            if context_data:
                GContext().set_by_dict(context_data)
                return True
            else:
                return False
        except Exception as e:
            print(f"装载{self.case_type}文件错误: {str(e)}")
            return False

    def load_files(self):
        """
        装载文件中的数据
        :return:
        """
        case_data_infos = []

        def for_file_in_dir(func):
            for file_name in file_names:
                file_path = os.path.join(self.case_dir, file_name)
                case_info = func(file_path)
                case_data_infos.append(case_info)

        # 获取 suite 文件夹下的所有 指定类型文件，并按文件名排序
        file_names = PathOperation().ls_all_file_by_type(self.case_dir, self.case_type)
        # 将 指定类型文件全部读取出来
        if self.case_type == 'yaml':
            for_file_in_dir(load_yaml)

        elif self.case_type == 'json':
            for_file_in_dir(load_json)
        return case_data_infos


def case_parser(case_type: str, case_dir: str, log: Log) -> Dict[str, Union[str, List[
    Dict[str, Union[str, Dict[str, str], List[Dict[str, Union[str, Dict[str, str], List[Dict[str, str]]]]]]]]]]:
    """
    核心运行器
    :param case_type:
    :param case_dir:
    :param log:
    :return:example dict:{
                        "case_names": str,
                        "case_infos":[{
                                        "context: {str:str}",
                                        "desc": str,
                                        "steps":[
                                            {
                                                'pre_script': str,
                                                'url': str,
                                                'data' :{str:str}
                                                'header': [{str:str}]
                                                'method': str,
                                                'assert_options':[{str:str}]
                                                'post_script': str
                                            }
                                        ]}]}
    """
    _type_list = ['yaml', 'json']

    if case_type in _type_list:
        case_infos = []
        case_names = []
        cs = CaseParser(case_type=case_type, case_dir=case_dir, log=log)
        try:
            # 第一步 根据文件类型，load case_dir下的 context
            cs.load_context_from_type()
            # 第二步  加载所有的文件路径
            case_data_infos = cs.load_files()
            # pprint(case_infos)
            # 第三步，将所有的文件解析成运行器可读的格式
            for case_info in case_data_infos:
                # 读取 DDTS 节点 --- 生成多组测试用例
                ddts = case_info.get("ddts", [])
                if len(ddts) > 0:
                    case_info.pop("ddts")

                if len(ddts) == 0:
                    case_infos.append(case_info)
                    case_names.append(case_info.get("desc", case_info))
                else:
                    # 循环生成多个用例执行对象，保存起来。
                    for ddt in ddts:
                        new_case = copy.deepcopy(case_info)
                        # 将数据读取后更新到 context 里面
                        context = new_case.get("context", {})
                        print(ddt)
                        ddt.update(context)
                        new_case.update({"context": ddt})
                        case_infos.append(new_case)
                        case_names.append(ddt["desc"])

            return {
                "case_infos": case_infos,
                "case_names": case_names
            }

        except Exception as e:

            cs.log.error(f'case_parser Error:{type(e).__name__} ErrorMsg:{e}')
            raise
    else:
        return {"case_name": [], "cases_info": []}


if __name__ == '__main__':
    from pprint import pprint

    from api_runner.extend.script.run_script import exec_script

    # from api_runner.core.globalContext import GContext

    data = case_parser('yaml', 'examples/suit_debug_yaml_1')

    script_data = data['case_infos'][0]['steps'][0]['pre_script']
    pprint(data['case_infos'][0]
           ['steps'][0]['pre_script'])

    exec_script(script_data, data['case_infos'][0]
    ['steps'][0], GContext())
    data1 = case_parser('json', 'examples/suit_debug_json_2')
    script_data = data1['case_infos'][0]['steps'][0]['pre_script']
    pprint(data1['case_infos'][0]
           ['steps'][0]['pre_script'])

    exec_script(script_data, data1['case_infos'][0]
    ['steps'][0], GContext())
