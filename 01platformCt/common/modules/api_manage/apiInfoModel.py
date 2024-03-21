# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiInfoModel.py
# Author:      Jakilo
# Datetime:    2024/2/18 10:23
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


from app import db


class ApiInfoModel(db.Model):
    __tablename__ = "t_api_info"
    id = db.Column(db.Integer, primary_key=True, comment='接口用例编号', autoincrement=True)
    project_id = db.Column(db.Integer, comment='项目ID')
    module_id = db.Column(db.Integer, comment='模块ID')
    api_name = db.Column(db.String(255), comment='接口名称')
    request_method = db.Column(db.String(255), comment='请求方法')
    request_url = db.Column(db.String(255), comment='请求地址')
    request_params = db.Column(db.String(255), comment='URL参数')
    request_headers = db.Column(db.Text(collation='utf8_general_ci'), comment='请求头')
    debug_vars = db.Column(db.Text(collation='utf8_general_ci'), comment='调试参数')
    request_form_datas = db.Column(db.String(255), comment='form-data')
    request_www_form_datas = db.Column(db.String(255), comment='www-form-data')
    request_json_data = db.Column(db.String(255), comment='json数据')
    pre_request = db.Column(db.String(255), comment='执行前事件')
    post_request = db.Column(db.String(255), comment='执行后事件')
    create_time = db.Column(db.DateTime, unique=True)
