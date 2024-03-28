# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     shellUtil.py
# Author:      Jakilo
# Datetime:    2024/3/4 10:38
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


import os
import subprocess
import time
import shutil

# from paramiko import SSHClient,AutoAddPolicy


# 本地命令类
class Shell:
    @staticmethod
    def invoke(cmd: str) -> str:
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o

    @staticmethod
    def command_output(remote_command: str) -> str:
        return subprocess.check_output(remote_command, shell=True, universal_newlines=True, encoding='GB2312',
                                       errors='ignore')

    @staticmethod
    def rmtree(path: os.path):
        shutil.rmtree(path)


# linux操作类
# class ConLinux:
#     def __init__(self, hostname, username, password=''):
#         self.shell = SSHClient()
#         # 取消安全认证
#         self.shell.set_missing_host_key_policy(AutoAddPolicy())
#         # 连接linux
#         print(f'准备连接{hostname}, {username}, {password}')
#         self.shell.connect(hostname=hostname, username=username, password=password)
#
#         self.channel = self.shell.invoke_shell()
#
#     def con_linux(self, command):
#         # 执行命令
#         stdin, stdout, stderr = self.shell.exec_command(command)
#         # 读取执行结果
#         result = stdout.read()
#         # 返回执行结果
#         return result
#
#     def invoke(self, command):
#         self.channel.send(command + '\n')
#         buff = ""
#         while not buff.strip(" ").endswith('2004h'):
#             time.sleep(1)
#             resp = self.channel.recv(9999).decode("ISO-8859-1")
#             buff += resp
#             print(resp)
#
#     def __del__(self):
#         self.shell.close()
