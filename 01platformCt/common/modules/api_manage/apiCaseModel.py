# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiCaseModel.py
# Author:      Jakilo
# Datetime:    2024/2/18 10:11
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


from app import db


class ApiCaseModel(db.Model):
    __tablename__ = "t_api_case"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_info_id = db.Column(db.Integer, nullable=False, comment="关联接口ID")
    collection_id = db.Column(db.Integer, nullable=False, comment="关联集合ID")
    param_data = db.Column(db.Text, comment="参数化运行")
    run_order = db.Column(db.Integer, nullable=False, comment="运行顺序")
    create_time = db.Column(db.DateTime, comment="创建时间")
