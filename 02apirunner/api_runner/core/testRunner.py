# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     testRunner.py
# Author:      Jakilo
# Datetime:    2024/1/18 11:47
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:  测试执行的入口
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from api_runner.core.testCasesPlugin import test_log_by_pytest
from api_runner.core.apiTestHandler import ApiTestHandler
from api_runner.core.globalContext import GContext
from api_runner.utils.varRender import refresh_var
from api_runner.extend.script.run_script import exec_script


class TestRunner:
    def test_case(self, case_info: dict, run_pytest_fix):
        """
        http 接口调用核心执行器
        是否需要添加一个pytest 运行装饰器，用来读取需要加载的配置信息
        :param case_info:
        :return:
        """
        steps = case_info.get('steps')
        # test_log_by_pytest.info(f'用例执行信息：\n{case_info}')
        context = case_info.get('context', None)
        if context:
            GContext().set_by_dict(context)
        ath = ApiTestHandler(*run_pytest_fix)

        for step in steps:
            # 1. 请求前 - 执行前置脚本(脚本也可以引用变量)
            pre_script = step.get("pre_script", None)
            if pre_script:
                refresh_var(pre_script, GContext().show_dict())
                exec_script(pre_script, step, GContext().show_dict())

            # 2. 请求前 - 所有请求相关的参数做个变量渲染
            request_content = {"url": step.get("url", None),
                               "method": step.get("method", None),
                               "params": step.get("params", None),
                               "data": step.get("data", None),
                               "json": step.get("json", None),
                               "headers": step.get("headers", None),
                               "cookies": step.get("cookies", None),
                               "timeout": step.get("timeout", None)}
            # 解决 cookie 等渲染问题
            request_content = eval(refresh_var(request_content, GContext().show_dict()))

            #  3.具体请求操作，发送 HTTP 请求，进行返回结果断言   --- 后期添加多挣请求方式支持，是否需要在这个位置封装？
            resp = ath.request_method(request_content)
            #  4.后置脚本(脚本也可以引用变量) 断言，参数提取
            #  断言，需要两个参数，一个 resp，一个断言参数
            ath.assert_method(step.get('assert_option'), resp)
            post_script = step.get("post_script", None)
            if post_script:
                # test_log_by_pytest.error(post_script)
                refresh_var(post_script, GContext().show_dict())
                exec_script(post_script, step, GContext().show_dict())
            #  5.是否要添加其他操作支持
