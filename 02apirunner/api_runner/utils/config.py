# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     config.py
# Author:      Jakilo
# Datetime:    2024/1/22 17:18
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from configparser import ConfigParser

from api_runner.utils.path import PathOperation


class NewConfigParser(ConfigParser):
    # 重写ConfigParser中自带的将写入option自动替换成小写的方法
    def optionxform(self, optionstr):
        return optionstr


class Config:
    def __init__(self, config_path='data/config/config.ini'):
        """
        初始化
        """
        self.path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
        # print(self.path_dir)
        self.config = NewConfigParser()
        self.conf_path = os.path.join(self.path_dir, config_path)
        # print(self.conf_path)
        self.config.read(self.conf_path, encoding='utf8')

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError(f"请确保配置文件存在！:{self.conf_path}")

    def get_conf(self, title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title, value)

    def set_conf(self, title, value, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def get_section(self, section_name: str) -> dict:
        """
        声明一个方法 接收一个章节名 返回这个章节的所有内容的键值对
        :param section_name:
        :return:
        """
        section_dict = {}
        # print('*'*20,section_name)
        if section_name in self.get_sections:
            items_list = self.config.items(section=section_name)
            for item_tuple in items_list:
                section_dict[item_tuple[0]] = item_tuple[1]

            return section_dict
        else:
            print(f'配置文件没有{section_name}章节名')
            return section_dict

    # 声明一个方法  返回当前文件的所有章节名列表
    @property
    def get_sections(self) -> list:
        return self.config.sections()

    # 声明一个方法 用于清空一个章节
    def clear_section(self, section_name: str) -> None:
        if self.config.has_section(section_name):
            self.config.remove_section(section_name)
            self.config.add_section(section_name)
            with open(self.conf_path, "w+") as f:
                return self.config.write(f)
