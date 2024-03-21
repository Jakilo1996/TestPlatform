# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     manage.py
# Author:      Jakiro
# Datetime:    2024/1/9 20:37
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from flask_script import Server,Manager

# 导入蓝图管理
from app import application, manage
from jobs.bgScdController import background_scheduler_run
import www


# 启动开发服务器


def main():
    background_scheduler_run()
    application.run(
    )

# 创建管理命令
Manager(application)

if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()
