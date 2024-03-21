# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     user.py
# Author:      Jakiro
# Datetime:    2024/1/9 23:01
# Description:
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from app import db
from flask_sqlalchemy.model import Model


# ORM 对象代表一张表
class User(db.Model):  # type: Model
    # 定义 User 表

    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.SmallInteger)
    create_time = db.Column(db.DateTime, unique=True)


# 定义 token 模型，这个其实是 session 的处理方案，token 不存入数据库中  弃用 session 方案
# class Token(db.Model):  # type: Model
#     # 定义 token 表
#     __tablename__ = 't_token'
#     id = db.Column(db.Integer, primary_key=True)
#     token_str = db.Column(db.String(255), unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)
#     expiration_date = db.Column(db.DateTime, nullable=False)
#     user = db.relationship('User', backref=db.backref('token', lazy='joined'))
