# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiCollectionController.py
# Author:      Jakilo
# Datetime:    2024/2/27 14:33
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


from flask import Blueprint, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length, Optional

from app import db, application
from web.utils.respUtil import RespModel
from web.utils.jwtUtil import JwtUtils
from web.utils.dbHandler import DbHandler
from web.utils.reqUtil import ReqModel, QueryByPageForm, DeleteAndQueryByIdApiForm, CustomValidation
from web.utils.runCaseHandler import run_case_collection
from common.modules.api_manage.apiCollectionModel import ApiCollectionModel
from common.modules.api_manage.apiInfoModel import ApiInfoModel
from common.modules.api_manage.apiCaseModel import ApiCaseModel
from common.modules.api_manage.apiHistoryModel import ApiHistoryModel

# 模块名称
module_name = "CtApiCollection"
module_model: db.Model = ApiCollectionModel
module_route = Blueprint(f'route_{module_name}', __name__)


@module_route.route(f'/{module_name}/QueryByPage', methods=["POST"])
@JwtUtils.token_required
def query_api_collection_by_page():
    try:
        with application.app_context():
            validate_reason = ReqModel.validate_req_form(QueryByPageForm, 'query_api_collection_by_page')
            if validate_reason[0]:
                page = validate_reason[1].get('page')
                page_size = validate_reason[1].get('pageSize')
                # 分页查询
                filter_list = []
                # 添加 项目筛选条件
                project_id = int(validate_reason[1].get("project_id", 0)) if validate_reason[1].get("project_id",
                                                                                                    0) else 0
                if project_id > 0:
                    filter_list.append(module_model.project_id == project_id)
                # 添加模块名称搜索条件
                query_module_name = request.json.get("collection_name", "")
                if query_module_name:
                    filter_list.append(module_model.module_name.like(f'%{module_name}%'))
                datas, total = DbHandler.query_by_page_by_filters(module_model, filter_list, page, page_size)

                return RespModel.ok_resp(obj_list=datas, obj_list_key="data", dict_t={"total": total}, msg='查询api模块成功')

    except Exception as e:
        return RespModel.internal_server_error_resp(e)


class QueryApiCollectionByIdForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])


@module_route.route(f'/{module_name}/QueryById', methods=["GET"])
@JwtUtils.token_required
def query_api_collection_by_id():
    try:
        with application.app_context():
            validate_tag, validate_form = ReqModel.validate_req_form(QueryApiCollectionByIdForm,
                                                                     'query_api_collection_by_id')
            if validate_tag:
                query_collection_id = validate_form.get('id')
                collection = DbHandler.query_by_id(module_model, query_collection_id)
            else:
                return RespModel.error_resp(msg=validate_form)
            if collection:
                return RespModel.ok_resp(obj_list=[collection], obj_list_key="data", msg='查询成功')
            else:
                return RespModel.ok_resp(msg='查询成功，数据为空')
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


class CreateApiCollectionForm(FlaskForm):
    project_id = IntegerField('project_id', validators=[Optional()])
    collection_name = StringField('collection_name', validators=[DataRequired()])
    collection_desc = StringField('collection_desc', validators=[DataRequired()])
    collection_env = StringField('collection_desc', validators=[CustomValidation.validate_json_format])
    collection_params = StringField('collection_desc', validators=[CustomValidation.validate_json_format])


@module_route.route(f'/{module_name}/CreateAction', methods=["POST"])
@JwtUtils.token_required
def create_api_collection_action():
    """
    新增 api project
    :return:
    """
    try:
        with application.app_context():
            validate_tag, validate_form = ReqModel.validate_req_form(CreateApiCollectionForm,
                                                                     'create_api_collection_action')
            if validate_tag:
                # validate_form.update({'create_time': datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')})
                create_context = validate_form
                create_api_case_id = DbHandler.create_action(module_model, create_context)
                return RespModel.ok_resp(msg='添加成功', dict_t={'id': create_api_case_id})
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


class UpdateApiCollectionForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    collection_name = StringField('collection_name', validators=[DataRequired()])
    collection_desc = StringField('collection_desc', validators=[DataRequired()])
    collection_env = StringField('collection_desc', validators=[CustomValidation.validate_json_format])
    collection_params = StringField('collection_desc', validators=[CustomValidation.validate_json_format])


@module_route.route(f'/{module_name}/UpdateAction', methods=["PUT"])
@JwtUtils.token_required
def update_api_collection_action():
    try:
        with application.app_context():
            print(request.json)
            validate_tag, validate_form = ReqModel.validate_req_form(UpdateApiCollectionForm,
                                                                     'update_api_collection_action')
            if validate_tag:
                update_collection_id = validate_form.get('id')
                if DbHandler.update_action_by_id(module_model, validate_form):
                    return RespModel.ok_resp(msg=f'api集合：{update_collection_id}修改成功')
                else:
                    return RespModel.error_resp(msg=f'api集合：{update_collection_id}未找到')
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


class DeleteApiCollectionForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])


@module_route.route(f'/{module_name}/DeleteAction', methods=["DELETE"])
@JwtUtils.token_required
def delete_api_collection_action():
    try:
        with application.app_context():
            validate_tag, validate_form = ReqModel.validate_req_form(DeleteApiCollectionForm,
                                                                     'delete_api_collection_action')
            if validate_tag:
                del_collection_id = validate_form.get('id')
                del_pro = DbHandler.delete_by_id_action(module_model, del_collection_id)
                if del_pro:
                    return RespModel.ok_resp(msg=f'api集合：{del_collection_id}删除成功')
                else:
                    return RespModel.error_resp(msg=f'api集合：{del_collection_id}未找到')
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)


@module_route.route(f'/{module_name}/ExecuteTestAction', methods=["GET"])
@JwtUtils.token_required
def execute_test_api_collection_action():
    print(request.args)
    try:
        with application.app_context():
            validate_tag, validate_form = ReqModel.validate_req_form(DeleteAndQueryByIdApiForm,
                                                                     'execute_test_api_collection_action')
            if validate_tag:
                # 1. 查询指定ID的集合数据
                execute_collection_id = validate_form.get('id')
                collection: ApiCollectionModel = DbHandler.query_by_id(module_model, execute_collection_id)
                if collection:
                    run_case_collection_tag, run_case_collection_str = run_case_collection(collection, ApiCaseModel,
                                                                                           ApiInfoModel,
                                                                                           ApiHistoryModel)
                    if run_case_collection_tag == 0:
                        return RespModel.error_resp(
                            msg=f'测试套件执行失败：{execute_collection_id}，执行发生错误{run_case_collection_str}')

                    else:
                        return RespModel.ok_resp(msg='请求成功', dict_t={'history_id': run_case_collection_tag})
                else:
                    return RespModel.error_resp(msg=f'api集合：{execute_collection_id}未找到')
            else:
                return RespModel.error_resp(msg=validate_form)
    except Exception as e:
        return RespModel.internal_server_error_resp(e)
