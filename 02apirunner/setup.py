# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     setup.py
# Author:      Jakilo
# Datetime:    2024/3/8 15:35
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

import setuptools
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
setuptools.setup(
    # 项目介绍
    name='ApiTestRun',
    # 版本号
    version='1',
    # author
    author='Jakilo',
    anthor_email='17709005281@163.com',
    description='sdp自动化测试框架',
    # 需要安装的第三方依赖
    install_requires=[
        "pytest",
        "jsonpath",
        "PyYAML",
        "pyyaml-include",
        "requests",
        "allure-pytest"
    ],
    # 此项很重要，如果不自动查找依赖包，会导致运行时的找不到包错误
    packages=setuptools.find_packages(),
    # py_modules=['conftest', 'main'],
    # package_data={'mypkg': ['data/*']},
    python_requires='>=3.6',
    # 可执行文件的函数入口
    entry_points={
        'console_scripts': [
            # 可执行文件的名称=执行的具体代码方法
            'ApiTestRun=api_runner.cli:run'
        ]
    },
    # data_files=[('data/config', ['data/config/config.ini'])],
    # 决定安装位置
    zip_safe=False,
    # 是否导入MANIFEST.in目录中的文件
    # include_package_data=True
)
