# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   02apirunner
# FileName:     functions.py
# Author:      Jakilo
# Datetime:    2024/1/26 14:05
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

def aes_encrypt(key, data):
    from api_runner.extend.crypto.aes_enrcypt import EncryptData

    """ AES 加密封装 """
    print("start ========= scripts")
    print("加密原文:", data)
    print("加密key:", key)
    eg = EncryptData(key)  # 这里密钥的长度必须是16的倍数
    res = eg.encrypt(str(data))
    print("密文:", res)
    return res


def sql_exec(type, db_config, sql):
    print("start=========")
    print("连接数据库:", db_config)
    print("执行SQL:", sql)
    result = None
    if type == 'mysql':
        # from apirunner.extend.database.SqlByMysql import query_all
        # result = query_all(db_config, sql)
        print(sql)
    print("SQL执行结果：", result)
    print("end=========")
    return result
