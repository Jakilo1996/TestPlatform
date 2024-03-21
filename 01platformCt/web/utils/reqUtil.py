# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     reqModel.py
# Author:      Jakilo
# Datetime:    2024/2/28 15:33
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import json
import re
from typing import Union, Tuple

from flask import request
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired
from wtforms import validators, IntegerField, StringField


class ReqModel:
    @staticmethod
    def validate_req_form(obj, pre_msg: str, msg: str = '参数错误') -> Tuple[bool, Union[dict, str]]:
        """

        :param obj: 参数验证定义FlaskForm类
        :param pre_msg: 错误返回前缀
        :param msg: 错误返回
        :return:
        """
        req_method = request.method

        if req_method in ["DELETE", "GET"]:
            validate_form = obj(request.args)

        elif req_method in ["POST", "PUT"]:
            # 传入 form 的写法 validate_form = obj(data=request.form)
            # 传入 json 的写法
            # print('before')
            # print(request.json)
            validate_form = obj(data=request.form)
            # print('after')

        else:
            return False, f'{pre_msg}请求类型验证不支持{req_method}'
        if not validate_form.validate():
            # 参数验证失败
            errors = validate_form.errors
            return False, f'{pre_msg}{msg}:{errors}'
        else:
            return True, validate_form.data


class DeleteAndQueryByIdApiForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])


class QueryByPageForm(FlaskForm):
    page = IntegerField('page', validators=[DataRequired()])
    pageSize = IntegerField('pageSize', validators=[DataRequired()])


class CustomValidation:
    @staticmethod
    def not_empty(form, field):
        """
        验证字符串可以为 0 不为空
        :param form:
        :param field:
        :return:
        """
        if not field.data and field.data != 0:
            raise ValidationError('This field is required.')

    @staticmethod
    def validate_json_format(form, field):
        """
        符合 json 格式的入参，允许空字符串
        :param form:
        :param field:
        :return: TODO 有问题
        """
        if field.data:
            print(field.data)
            print(form)
            print(type(field.data))
            try:
                pass
                # json.loads(field.data)
            except json.JSONDecodeError as e:
                raise ValidationError("Invalid JSON format: {}".format(e))
            except TypeError as e:
                raise ValidationError("Invalid JSON format: {}".format(e))

    @staticmethod
    def validate_http_methods(form, field):
        """
        验证字符串属于 http 请求头
        :param form:
        :param field:
        :return:
        """
        validate_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
        if field.data.upper() not in validate_methods:
            raise ValidationError('Invalid HTTP method')

    @staticmethod
    def validate_http_url(form, field):
        """
        验证字符串符合 http url 格式定义
        :param form:
        :param field:
        :return:
        """
        url_pattern = re.compile(
            r'^(https?://)?'  # http:// 或 https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # 域名
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP 地址
            r'(?::\d+)?'  # 端口号（可选）
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not url_pattern.match(field.data):
            raise ValidationError('Invalid HTTP URL')

    @staticmethod
    def validate_http_headers(form, field):
        """
        验证字符串是否是可以 JSON反序列化的列表或者空列表对象，列表中的元素为字典且满足Http请求头要求
        :param form:
        :param field:
        :return:
        """
        if field.data:
            try:
                # 尝试解析字符串为 JSON 格式
                headers = json.loads(field.data)
                # 验证 headers 是否为列表或空列表
                if not isinstance(headers, list):
                    raise validators.ValidationError('HTTP headers must be a list')
                else:
                    for header in headers:
                        # 检查 header 是否符合 HTTP 请求头的格式
                        if not re.match(r'^[a-zA-Z0-9-]+: .+$', header):
                            raise validators.ValidationError(f'Invalid HTTP header format: {header}')
            except json.JSONDecodeError:
                raise validators.ValidationError('Invalid JSON format')
