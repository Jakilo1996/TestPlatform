# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     testReportModel.py
# Author:      Jakilo
# Datetime:    2024/3/14 21:01
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

from app import db
# 表设计
# id: 主键，自增长的唯一标识符
# uuid: 测试报告的唯一标识符，通常采用 UUID 格式
# name: 测试报告的名称
# description: 测试报告的描述
# path: 测试报告存储的路径
# created_at: 测试报告创建的时间

# 业务设计
# run_collection 运行完成后，弹出当前的运行结果，以及是否保存，debug_case 仅生成临时的文件，然后删除文件以及映射关系

# 定义 TestReportModel 模型类
class TestReportModel(db.Model):
    __tablename__ = 't_test_report'  # 数据库表名
    # 测试报告与测试 log 的关系是一对一
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自增长的唯一标识符
    uuid = db.Column(db.String(36), nullable=False, unique=True)  # 测试报告的唯一标识符，UUID 格式
    name = db.Column(db.String(255))  # 测试报告的名称
    description = db.Column(db.Text)  # 测试报告的描述
    path = db.Column(db.String(255), nullable=False)  # 测试报告存储的路径
    created_at = db.Column(db.DateTime, nullable=False)  # 测试报告创建的时间