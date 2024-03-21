# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiProjectController.py
# Author:      Jakilo
# Datetime:    2024/2/18 10:30
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description: Api 项目管理
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from datetime import datetime

from flask import Blueprint, request

from app import db, application
from web.utils.respUtil import RespModel
from web.utils.jwtUtil import JwtUtils
from web.utils.dbHandler import DbHandler
from common.modules.api_manage.apiProjectModel import ApiProjectModel

# 模块名称
module_name = "CtApiProject"
module_model: db.Model = ApiProjectModel
module_route = Blueprint(f'route_{module_name}', __name__)


@module_route.route(f'/{module_name}/QueryByPage', methods=["POST"])
@JwtUtils.token_required
def query_api_project_by_page():
    try:
        with application.app_context():
            page = int(request.json["page"])
            page_size = int(request.json["pageSize"])
            # 分页查询
            filter_list = []
            datas, total = DbHandler.query_by_page_by_filters(module_model, filter_list, page, page_size)

            return RespModel.ok_resp(obj_list=datas, obj_list_key="data", dict_t={"total": total}, msg='查询api 项目成功')
    except ValueError as e:
        return RespModel.error_resp(msg='query_api_project_by_page 参数错误')


@module_route.route(f'/{module_name}/QueryById', methods=["GET"])
@JwtUtils.token_required
def query_api_project_by_id():
    try:
        req_args = request.args
        proj_id = int(req_args.get('id'))
        with application.app_context():
            proj = DbHandler.query_by_id(module_model, proj_id)
            if proj:
                return RespModel.ok_resp(obj_list=[proj], obj_list_key="data", msg='查询api 项目成功')
            else:
                return RespModel.ok_resp(msg='查询成功，数据为空')
    except ValueError as e:
        return RespModel.error_resp(msg='参数错误')


@module_route.route(f'/{module_name}/QueryAll', methods=["GET"])
@JwtUtils.token_required
def query_api_project_all():
    try:
        with application.app_context():
            proj_list = DbHandler.query_all(module_model)
            if proj_list:
                return RespModel.ok_resp(obj_list=proj_list, obj_list_key="data", msg='查询成功')
            else:
                return RespModel.ok_resp(msg='不存在任何项目')
    except ValueError as e:
        return RespModel.internal_server_error_resp(e)


@module_route.route(f'/{module_name}/CreateAction', methods=["POST"])
@JwtUtils.token_required
def create_api_project_action():
    """
    新增 api project
    :return:
    """
    try:
        with application.app_context():
            create_data: dict = request.json
            create_data.update({'create_time': datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')})
            data_id = DbHandler.create_action(module_model, create_data)
        return RespModel.ok_resp(msg='添加成功', dict_t={'id': data_id})
    except ValueError as e:
        return RespModel.error_resp(msg='参数错误')


@module_route.route(f'/{module_name}/UpdateAction', methods=["PUT"])
@JwtUtils.token_required
def update_api_project_action():
    try:
        with application.app_context():
            update_proj_id = request.json.get('id')
            if DbHandler.update_action_by_id(module_model, dict(request.json)):
                return RespModel.ok_resp(msg=f'api项目{update_proj_id}修改成功')
            else:
                return RespModel.error_resp(msg=f'项目id：{update_proj_id}不存在')

    except ValueError as e:
        return RespModel.error_resp(msg='参数错误')


@module_route.route(f'/{module_name}/DeleteAction', methods=["DELETE"])
@JwtUtils.token_required
def delete_api_project_action():
    try:
        with application.app_context():
            del_pro_id = int(request.args.get('id', None))
            if del_pro_id:
                del_pro = DbHandler.delete_by_id_action(module_model, del_pro_id)
                if del_pro:
                    return RespModel.ok_resp(msg=f'api项目：{del_pro_id}删除成功')
                else:
                    return RespModel.error_resp(msg=f'api项目：{del_pro_id}未找到')
            else:
                return RespModel.error_resp(msg=f'DeleteAction：id参数错误')
    except ValueError as e:
        return RespModel.error_resp(msg='参数错误')
