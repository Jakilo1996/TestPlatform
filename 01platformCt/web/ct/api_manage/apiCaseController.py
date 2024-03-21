# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiCaseController.py
# Author:      Jakilo
# Datetime:    2024/1/17 18:25
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


from datetime import datetime

from flask import Blueprint, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app import db, application
from web.utils.respUtil import RespModel
from web.utils.jwtUtil import JwtUtils
from web.utils.dbHandler import DbHandler
from web.utils.reqUtil import ReqModel, CustomValidation, QueryByPageForm, DeleteAndQueryByIdApiForm
from common.modules.api_manage.apiCaseModel import ApiCaseModel
from common.modules.api_manage.apiInfoModel import ApiInfoModel
from common.lib.funcBase import BaseTools

# 模块名称X
module_name = "CtApiCase"
module_model: db.Model = ApiCaseModel
module_route = Blueprint(f'route_{module_name}', __name__)


class QueryApiCaseByPageForm(QueryByPageForm):
    collection_id = IntegerField('collection_id', validators=[DataRequired()])


@module_route.route(f'/{module_name}/QueryByPage', methods=["POST"])
@JwtUtils.token_required
def query_api_case_by_page():
    try:
        with application.app_context():
            validate_tag, validate_form = ReqModel.validate_req_form(QueryApiCaseByPageForm,
                                                                     'query_api_collection_by_page')
            if validate_tag:
                # 分页查询
                page = validate_form.get('page')
                page_size = validate_form.get('pageSize')
                # 测试集合信息
                collection_id = validate_form.get('collection_id')
                filter_list = [module_model.collection_id == collection_id]
                # 添加测试集合
                # 添加 项目筛选条件
                project_id = validate_form.get("project_id", 0)

                # 没有实现双条件查询
                if project_id > 0:
                    filter_list.append(module_model.project_id == project_id)
                # 添加模块名称搜索条件
                query_module_name = validate_form.get("module_name", "")
                if query_module_name:
                    filter_list.append(module_model.module_name.like(f'%{module_name}%'))

                datas, total = DbHandler.query_by_page_by_filters(module_model, filter_list, page, page_size)
                results = []
                for case in datas:
                    # print(case.id)
                    api_info = DbHandler.query_by_id(ApiInfoModel, _id=case.api_info_id)
                    if api_info:
                        result = BaseTools.get_attr(api_info, ['id'])
                        result.update(BaseTools.get_attr(case))
                        results.append(result)
                    else:
                        application.logger.error(f'api_case{case.id}绑定的 api_info{case.api_info_id} 未找到')
                        return RespModel.error_resp('api_case绑定的 api_info 未找到')
                return RespModel.ok_resp_simple_list(results, '查询apiCase成功', total)
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


@module_route.route(f'/{module_name}/QueryById', methods=["GET"])
@JwtUtils.token_required
def query_api_case_by_id():
    try:
        req_args = request.args
        proj_id = int(req_args.get('id'))
        with application.app_context():
            proj = DbHandler.query_by_id(module_model, proj_id)
            if proj:
                return RespModel.ok_resp(obj_list=proj, obj_list_key="data", msg='查询成功')
            else:
                return RespModel.ok_resp(msg='查询成功，数据为空')
    except ValueError as e:
        return RespModel.error_resp(msg='参数错误')


class CreateApiCaseForm(FlaskForm):
    api_info_id = IntegerField('api_info_id', validators=[DataRequired()])
    collection_id = IntegerField('collection_id', validators=[DataRequired()])
    param_data = StringField('param_data', validators=[Optional(), CustomValidation.validate_json_format])
    run_order = IntegerField('run_order', validators=[CustomValidation.not_empty, NumberRange(max=10000)])


@module_route.route(f'/{module_name}/CreateAction', methods=["POST"])
@JwtUtils.token_required
def create_api_case_action():
    """
    新增 api_case
    :return:
    """
    try:
        with application.app_context():
            validate_tag, validate_form = ReqModel.validate_req_form(CreateApiCaseForm, 'create_api_case_action')
            if validate_tag:
                validate_form.update({'create_time': datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')})
                create_context = validate_form
                create_api_case_id = DbHandler.create_action(module_model, create_context)
                return RespModel.ok_resp(msg='添加成功', dict_t={'id': create_api_case_id})
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


class UpdateApiCaseForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    run_order = IntegerField('run_order', validators=[CustomValidation.not_empty, NumberRange(max=10000)])
    param_data = StringField('param_data', validators=[Optional(), CustomValidation.validate_json_format])


@module_route.route(f'/{module_name}/UpdateAction', methods=["PUT"])
@JwtUtils.token_required
def update_api_case_action():
    try:
        with application.app_context():
            print(request.json)
            validate_tag, validate_form = ReqModel.validate_req_form(UpdateApiCaseForm, 'update_api_case_action')
            if validate_tag:
                update_api_case_id = validate_form.get('id')
                if DbHandler.update_action_by_id(module_model, validate_form):
                    return RespModel.ok_resp(msg=f'更新 api_case:{update_api_case_id}成功')
                else:
                    return RespModel.error_resp(msg=f'更新 api_case失败，{update_api_case_id}不存在')
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


@module_route.route(f'/{module_name}/DeleteAction', methods=["DELETE"])
@JwtUtils.token_required
def delete_api_case_action():
    try:
        with application.app_context():
            del_module_id = int(request.args.get('id', None))
            if del_module_id:
                del_pro = DbHandler.delete_by_id_action(module_model, del_module_id)
                if del_pro:
                    return RespModel.ok_resp(msg=f'api模块：{del_module_id}删除成功')
                else:
                    return RespModel.error_resp(msg=f'api模块：{del_module_id}未找到')
            else:
                return RespModel.error_resp(msg=f'DeleteAction：id参数错误')
    except ValueError as e:
        return RespModel.error_resp(msg='参数错误')
