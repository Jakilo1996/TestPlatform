# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiHistoryModel.py
# Author:      Jakilo
# Datetime:    2024/2/18 10:03
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


from app import db


class ApiHistoryModel(db.Model):
    __tablename__ = "t_api_history"

    id = db.Column(db.Integer, primary_key=True, comment='记录编号')
    collection_id = db.Column(db.Integer, comment='关联t_api_collection表主键id')
    history_desc = db.Column(db.String(255), comment='运行记录简述')
    history_detail = db.Column(db.String(255), comment='运行详细记录')
    create_time = db.Column(db.DateTime, comment='创建时间')