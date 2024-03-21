# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     testCasesPlugin.py
# Author:      Jakilo
# Datetime:    2024/1/18 13:22
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import pytest

from api_runner.utils.log import Log

test_log_by_pytest = Log(module='debug')


class TestCasesPlugin:
    """
    调用 pytest 的钩子函数，进行 pytest 命令行配置操作
    """

    def pytest_addoption(self, parser):
        """
        pytest : 初始化时调用
        增加pytest运行的配置项
        """

        parser.addoption(
            "--type", action="store", default="yaml", help="测试用例类型"
        )
        parser.addoption(
            "--cases", action="store", default="../examples", help="测试用例目录"
        )
        parser.addoption(
            "--debug_mode", action="store", default=False, help="调试测试执行选项"
        )
        parser.addoption(
            "--debug_init", action="store", default=False, help="调试初始化case"
        )
        parser.addoption("--pro", action="store", help='测试的产品线')

    def pytest_collection_modifyitems(self, session, config, items):
        """
        pytest:用例收集完成时调用
        解决 ids unicode 编码问题
        :param session:
        :param config:测试的配置
        :param items:用例 items
        :return:
        """

        def change(item_str: str) -> str:
            return item_str.encode('utf-8').decode('unicode_escape')

        for item in items:
            item.name = change(item.name)
            item._nodeid = change(item._nodeid)
            test_log_by_pytest.info(f'{item._nodeid},{item.name}')

    def pytest_generate_tests(self, metafunc):
        """
        method_meta: 运行的方法信息
        """
        # 函数中导入 解决循环导入的问题
        from api_runner.core.caseParserController import case_parser
        # 读取用户传过来的参数
        case_type = metafunc.config.getoption("type")
        cases_dir = metafunc.config.getoption("cases")
        # 读取测试用例
        data = case_parser(case_type, cases_dir, test_log_by_pytest)
        # 把测试用例作为参数化，交给 runner 执行
        if "case_info" in metafunc.fixturenames:
            metafunc.parametrize("case_info", data['case_infos'], ids=data['case_names'])

    # def pytest_assertion_pass(self, item, lineno, orig, expl):
    #     '''
    #     断言通过时执行的钩子函数
    #     :param item:
    #     :param lineno:
    #     :param orig:
    #     :param expl:
    #     :return:
    #     '''
    #     pass

    # def pytest_sessionfinish(self,session,exitstatus):
    #     '''
    #     在整个测试运行完成后调用，就在将退出状态返回给系统之前
    #     :param session:
    #     :param exitstatus:
    #     :return:
    #     '''
    #     session._setupstate.teardown_all()

    def pytest_assertrepr_compare(self, op, left, right) -> list:
        """
        pytest:断言失败时执行的钩子函数， 返回用例断言失败，表达式中比较内容的解释
        重写assert断言的报错信息
        :param op: 运算符
        :param left: 左边的元素
        :param right: 右边的元素
        :return:报错信息[]
        """
        if op == '==':
            if not isinstance(right, type(left)):
                return [
                    f'断言错误，期望结果与实际结果的数据类型不一致， 期望数据类型为:{type(right)} 实际值为:{type(left)}',
                    f'期望值为：{right},实际值为：{left}'
                ]
            else:
                return [
                    f'断言错误，期望值与实际值不一致，期望值为：{right}实际值为：{left}'
                ]

        elif op == 'in':
            if isinstance(right, set) or isinstance(right, tuple) or isinstance(right, list):
                if isinstance(right, set):
                    return [
                        f'断言错误，期望{left}为集合{right}的一个元素，实际上集合{right}中没有{left}元素'
                    ]
                elif isinstance(right, tuple):
                    return [
                        f'断言错误，期望{left}为元祖{right}的一个元素，实际上元祖{right}中没有{left}元素'
                    ]
                elif isinstance(right, list):
                    return [
                        f'断言错误，期望{left}为列表{right}的一个元素，实际上列表{right}中没有{left}元素'
                    ]

            elif isinstance(right, str) and isinstance(left, str):
                return [
                    f'断言错误，期望{left}是{right}的子串，实际{left}不是{right}的子串'
                ]

            elif isinstance(right, dict):
                return [
                    f'断言错误，期望{left}是字典{right}的key列表{right.keys()}的一个key，实际字典{right}中没有值为{left}的key'
                ]
            else:
                return [
                    f'期望 {left} 是 {right} 中的一部分，实际上 {left} 并不是 {right} 的一部分'
                ]

        elif op == 'not in':
            if isinstance(right, set) or isinstance(right, tuple) or isinstance(right, list):
                if isinstance(right, set):
                    return [
                        f'断言错误，期望{left}不是集合{right}的一个元素，实际上集合{right}中有{left}元素'
                    ]
                elif isinstance(right, tuple):
                    return [
                        f'断言错误，期望{left}不是元祖{right}的一个元素，实际上元祖{right}中有{left}元素'
                    ]
                elif isinstance(right, list):
                    return [
                        f'断言错误，期望{left}不是列表{right}的一个元素，实际上列表{right}中有{left}元素'
                    ]

            elif isinstance(right, str) and isinstance(left, str):
                return [
                    f'断言错误，期望{left}不是{right}的子串，实际{left}是{right}的子串'
                ]

            elif isinstance(right, dict):
                return [
                    f'断言错误，期望{left}不是字典{right}的key列表{right.keys()}的一个key，实际字典{right}中有值为{left}的key'
                ]
            else:
                return [
                    f'期望 {left} 不是 {right} 中的一部分，实际上 {left} 是 {right} 的一部分'
                ]

        elif op == '>':
            if not isinstance(right, type(left)):
                return [
                    f'断言错误，期望结果与实际结果的数据类型不一致， 期望数据类型为:{type(right)} 实际值为:{type(left)}',
                    f'期望值为：{right},实际值为：{left}'
                ]
            else:
                return [
                    f'断言错误，期望{left}大于{right},实际{left}不大于{right}'
                ]

        elif op == '<':
            if not isinstance(right, type(left)):
                return [
                    f'断言错误，期望结果与实际结果的数据类型不一致， 期望数据类型为:{type(right)} 实际值为:{type(left)}',
                    f'期望值为：{right},实际值为：{left}'
                ]
            else:
                return [
                    f'断言错误，期望{left}小于{right},实际{left}不小于{right}'
                ]

        elif op == '>=':
            if not isinstance(right, type(left)):
                return [
                    f'断言错误，期望结果与实际结果的数据类型不一致， 期望数据类型为:{type(right)} 实际值为:{type(left)}',
                    f'期望值为：{right},实际值为：{left}'
                ]
            else:
                return [
                    f'断言错误，期望{left}大于等于{right},实际{left}不大于等于{right}'
                ]

        elif op == '<=':
            if not isinstance(right, type(left)):
                return [
                    f'断言错误，期望结果与实际结果的数据类型不一致， 期望数据类型为:{type(right)} 实际值为:{type(left)}',
                    f'期望值为：{right},实际值为：{left}'
                ]
            else:
                return [
                    f'断言错误，期望{left}小于等于{right},实际{left}不小于等于{right}'
                ]

        elif op == "!=":
            if not isinstance(right, type(left)):
                return [
                    f'断言错误，期望结果与实际结果的数据类型不一致， 期望数据类型为:{type(right)} 实际值为:{type(left)}',
                    f'期望值为：{right},实际值为：{left}'
                ]
            else:
                return [
                    f'断言错误，期望值{left}与实际值{right}不相等,实际期望值{left}等于实际值{right}'
                ]
        else:
            return ['不支持断言类型']

    @pytest.fixture
    def run_pytest_fix(self, request, pytestconfig):
        test_log_by_pytest.info(
            f'in config_fix{request.module.__name__}，{pytestconfig.getoption("--type")}，')
        # print('in config_fix')
        yield pytestconfig.option, test_log_by_pytest

    def run_pytest_fix_example(self, request, pytestconfig, recwarn, tmp_path, monkeypatch):
        test_log_by_pytest.info(
            f'in config_fix{request.module.__name__}，{pytestconfig.getoption("--type")}，{tmp_path.name}')
        # print('in config_fix')
        yield pytestconfig.config.__item__, test_log_by_pytest


if __name__ == '__main__':
    pass
