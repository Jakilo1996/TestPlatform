# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiCollectionModel.py
# Author:      Jakilo
# Datetime:    2024/2/18 10:07
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


from app import db


class ApiCollectionModel(db.Model):
    __tablename__ = "t_api_collection"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, default=None)
    collection_name = db.Column(db.String(255), default=None)
    collection_desc = db.Column(db.String(255), default=None)
    collection_env = db.Column(db.String(255), default=None)
    collection_params = db.Column(db.String(255), default=None)
    create_time = db.Column(db.DateTime, default=None)
