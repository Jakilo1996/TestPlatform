# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiInfoController.py
# Author:      Jakilo
# Datetime:    2024/2/27 14:34
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:  apiInfo 管理
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

from datetime import datetime

from flask import Blueprint, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList
from wtforms.validators import DataRequired, Length, Optional, NumberRange

from app import db, application
from web.utils.respUtil import RespModel
from web.utils.reqUtil import ReqModel, CustomValidation, DeleteAndQueryByIdApiForm, QueryByPageForm
from web.utils.jwtUtil import JwtUtils
from web.utils.dbHandler import DbHandler
from web.utils.runCaseHandler import run_debug_case_info
from common.modules.api_manage.apiInfoModel import ApiInfoModel

# 模块名称
module_name = "CtApiInfo"
module_model: db.Model = ApiInfoModel
module_route = Blueprint(f'route_{module_name}', __name__)


@module_route.route(f'/{module_name}/QueryByPage', methods=["POST"])
@JwtUtils.token_required
def query_api_info_by_page():
    try:
        print(request.json)
        with application.app_context():
            validate_tag, validate_form = ReqModel.validate_req_form(QueryByPageForm,
                                                                     'query_api_info_by_page')
            if validate_tag:
                # 分页查询
                page = validate_form.get('page')
                page_size = validate_form.get('pageSize')
                # 分页查询
                filter_list = []
                # 添加 项目筛选条件
                project_id = validate_form.get('project_id')
                module_id = validate_form.get('module_id')
                # 没有实现双条件查询
                if project_id:
                    filter_list.append(module_model.project_id == project_id)
                if module_id:
                    filter_list.append(module_model.module_id == module_id)
                # 添加模块名称搜索条件
                query_api_info_name = request.json.get("api_name", "")
                if query_api_info_name:
                    filter_list.append(module_model.api_name.like(f'%{query_api_info_name}%'))

                datas, total = DbHandler.query_by_page_by_filters(module_model, filter_list, page, page_size)
                return RespModel.ok_resp(obj_list=datas, obj_list_key="data", dict_t={"total": total}, msg='查询api信息成功')
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


@module_route.route(f'/{module_name}/QueryById', methods=["GET"])
@JwtUtils.token_required
def query_api_info_by_id():
    try:
        with application.app_context():
            print(request.args)
            validate_tag, validate_form = ReqModel.validate_req_form(DeleteAndQueryByIdApiForm, 'query_api_info_by_id')
            if validate_tag:
                query_id = validate_form.get('id')
                query_data = DbHandler.query_by_id(module_model, query_id)
                if query_data:
                    return RespModel.ok_resp(obj_list=[query_data], obj_list_key="data", msg='查询成功')
                else:
                    return RespModel.ok_resp(msg='查询成功，数据为空')
            else:
                return RespModel.error_resp(validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


class CreateApiInfoForm(FlaskForm):
    id = IntegerField('id', validators=[Optional(), NumberRange(max=99999999)])
    project_id = IntegerField('project_id', validators=[Optional(), NumberRange(max=99999999)])
    module_id = IntegerField('project_id', validators=[Optional(), NumberRange(max=99999999)])
    api_name = StringField('collection_name', validators=[DataRequired(), Length(max=255)])
    request_method = StringField('request_method', validators=[CustomValidation.validate_http_methods, Length(max=255)])
    request_url = StringField('request_url', validators=[CustomValidation.validate_http_url, Length(max=255)])
    request_headers = StringField('request_headers',
                                  validators=[CustomValidation.validate_http_headers, Length(max=255)])
    debug_vars = StringField('debug_vars', validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_form_datas = StringField('request_form_datas',
                                     validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_www_form_datas = StringField('request_www_form_data',
                                         validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_json_data = StringField('request_json_data',
                                    validators=[CustomValidation.validate_json_format, Length(max=255)])
    pre_request = StringField('pre_request', validators=[Optional(), Length(max=255)])
    post_request = StringField('pre_request', validators=[Optional(), Length(max=255)])


@module_route.route(f'/{module_name}/CreateAction', methods=["POST"])
@JwtUtils.token_required
def create_api_info_action():
    """
    新增 api project
    :return:
    """
    try:
        with application.app_context():
            validate_tag, validate_form = ReqModel.validate_req_form(CreateApiInfoForm, 'create_api_info_action')
            if validate_tag:
                validate_form.update({'create_time': datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')})
                create_api_info_id = DbHandler.create_action(module_model, validate_form)
                return RespModel.ok_resp(msg='创建api_info成功', dict_t={'id': create_api_info_id})
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


class UpdateApiInfoForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired(), NumberRange(max=99999999)])
    project_id = IntegerField('project_id', validators=[Optional(), NumberRange(max=99999999)])
    module_id = IntegerField('project_id', validators=[Optional(), NumberRange(max=99999999)])
    api_name = StringField('collection_name', validators=[DataRequired(), Length(max=255)])
    request_method = StringField('request_method', validators=[CustomValidation.validate_http_methods, Length(max=255)])
    request_url = StringField('request_url', validators=[CustomValidation.validate_http_url, Length(max=255)])
    request_headers = StringField('request_headers',
                                  validators=[CustomValidation.validate_http_headers, Length(max=255)])
    debug_vars = StringField('debug_vars', validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_form_datas = StringField('request_form_datas',
                                     validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_www_form_data = StringField('request_www_form_data',
                                        validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_json_data = StringField('request_json_data',
                                    validators=[CustomValidation.validate_json_format, Length(max=255)])
    pre_request = StringField('pre_request', validators=[Optional(), Length(max=255)])
    post_request = StringField('pre_request', validators=[Optional(), Length(max=255)])


@module_route.route(f'/{module_name}/UpdateAction', methods=["PUT"])
@JwtUtils.token_required
def update_api_info_action():
    try:
        with application.app_context():
            print(request.json)
            validate_tag, validate_form = ReqModel.validate_req_form(UpdateApiInfoForm, 'update_api_info_action')
            if validate_tag:
                update_id = validate_form.get('id')
                if DbHandler.update_action_by_id(module_model, validate_form):
                    return RespModel.ok_resp(msg=f'更新 api_case:{update_id}成功')
                else:
                    return RespModel.error_resp(msg=f'更新 api_case失败，{update_id}不存在')
            else:
                return RespModel.error_resp(validate_form)

    except Exception as e:
        return RespModel.internal_server_error_resp(e)


@module_route.route(f'/{module_name}/DeleteAction', methods=["DELETE"])
@JwtUtils.token_required
def delete_api_info_action():
    try:
        with application.app_context():
            print(request.json)
            validate_tag, validate_form = ReqModel.validate_req_form(DeleteAndQueryByIdApiForm,
                                                                     'delete_api_info_action')
            if validate_tag:
                del_id = validate_form.get('id')
                del_tag = DbHandler.delete_by_id_action(module_model, del_id)
                if del_tag:
                    return RespModel.ok_resp(msg=f'api_info：{del_id}删除成功')
                else:
                    return RespModel.error_resp(msg=f'api_info：{del_id}未找到')
            else:
                return RespModel.error_resp(validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


class DebugApiInfoForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired(), NumberRange(max=99999999)])
    project_id = IntegerField('project_id', validators=[Optional(), NumberRange(max=99999999)])
    module_id = IntegerField('project_id', validators=[Optional(), NumberRange(max=99999999)])
    api_name = StringField('collection_name', validators=[DataRequired(), Length(max=255)])
    request_method = StringField('request_method', validators=[CustomValidation.validate_http_methods, Length(max=255)])
    request_url = StringField('request_url', validators=[CustomValidation.validate_http_url, Length(max=255)])
    request_params = StringField('request_params', validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_headers = StringField('request_headers',
                                  validators=[CustomValidation.validate_http_headers, Length(max=255)])
    debug_vars = FieldList('debug_vars', validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_form_datas = StringField('request_form_datas',
                                     validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_www_form_datas = StringField('request_www_form_datas',
                                         validators=[CustomValidation.validate_json_format, Length(max=255)])
    request_json_data = StringField('request_json_data',
                                    validators=[CustomValidation.validate_json_format, Length(max=255)])
    pre_request = StringField('pre_request', validators=[Optional(), Length(max=255)])
    post_request = StringField('pre_request', validators=[Optional(), Length(max=255)])


@module_route.route(f'/{module_name}/DebugExecuteAction', methods=["POST"])
@JwtUtils.token_required
def debug_api_info_action():
    """
    解决问题：
        文件及配置路径生成；
        将请求中的 Api 信息及测试参数信息保存到测试套件的对应文件夹；
        执行测试；
        回收测试文件，保存测试报告
    需要考虑的问题：
        如何进行测试套件生成的封装，这块是可以复用的
        将 API 信息以及 WEB 自动测试信息封装到同一套套件的可能性
        将测试执行后操作进行封装
    请求参数
    {'id': 12, 'project_id': 15, 'module_id': 11, 'api_name': '测试百度', 'request_method': 'GET',
     'request_url': 'www.baidu.com', 'request_params': [], 'request_headers': [], 'debug_vars': [],
     'request_form_datas': [], 'request_www_form_datas': [], 'requests_json_data': '', 'pre_request': '',
      'post_request': ''}
    :return:
    """
    try:
        with application.app_context():
            # validate_tag, validate_form = ReqModel.validate_req_form(DebugApiInfoForm, 'debug_api_info_action')
            # print(validate_form)
            validate_tag = 1
            validate_form = request.json
            if validate_tag:
                # 接收前端传递过来的 ApiInfo
                api_info = module_model(**validate_form,
                                        create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))
                # 执行测试
                command_output = run_debug_case_info(api_info)
                return RespModel.ok_resp(msg="接口调试执行结束", dict_t={"output": command_output})
            else:
                return RespModel.error_resp(validate_form)
    except Exception as e:
        print(e)
        return RespModel.error_resp(msg=f"执行出现错误：{e}")
