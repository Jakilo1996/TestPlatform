# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     timeBase.py
# Author:      Jakilo
# Datetime:    2024/3/18 17:11
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import time
from functools import reduce
from datetime import datetime, timedelta


class TimeBase:
    @staticmethod
    def generate_current_time() -> list:
        """
        声明一个函数，用来生成当前时间，并返回两个数
        :return:第一个为 year-month-day 第二个为 hour-min
        """
        return list(map(lambda i: reduce(lambda x, y: str(x) + '-' + str(y), i), list(
            map(lambda i: [eval(f"datetime.now().{x}") for x in i], [('year', 'month', 'day'), ('hour', 'minute')]))))

    @staticmethod
    def generate_current_strf_time():
        """
        按照 '%Y-%m-%d/%H:%M:%S' 生成当前时间，一般用作更新以及创建数据
        :return:
        """
        return datetime.strftime(datetime.today(), '%Y-%m-%d/%H:%M:%S')

    # 获取当前日期
    @staticmethod
    def get_current_date():
        return datetime.now()

    # 计算目标日期为当前日期减去两个月
    @staticmethod
    def calculate_target_date(current_date, **kwargs):
        # days，months
        return current_date - timedelta(**kwargs)

    @staticmethod
    def extract_str_date(_str:str):
        # 提取字符串日期信息
        file_date_str = _str.split('-')[-1]
        return datetime.strptime(file_date_str, "%Y-%m-%d")

if __name__ == '__main__':
    print(TimeBase.extract_str_date('a-2-4.txt'))