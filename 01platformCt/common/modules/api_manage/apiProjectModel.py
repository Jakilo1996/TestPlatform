# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiProjectModel.py
# Author:      Jakilo
# Datetime:    2024/2/18 09:56
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


from app import db


class ApiProjectModel(db.Model):
    __tablename__ = "t_api_project"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(255))
    project_desc = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
