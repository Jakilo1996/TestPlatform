# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     apiHistoryController.py
# Author:      Jakilo
# Datetime:    2024/2/27 14:32
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


from flask import Blueprint, request, send_from_directory

from app import db, application
from web.utils.respUtil import RespModel
from web.utils.jwtUtil import JwtUtils
from web.utils.dbHandler import DbHandler
from common.modules.api_manage.apiHistoryModel import ApiHistoryModel

# 模块名称
module_name = "CtApiHistory"
module_model: db.Model = ApiHistoryModel
module_route = Blueprint(f'route_{module_name}', __name__)


@module_route.route(f'/{module_name}/<path:_dir>/<filename>', methods=["GET"])
@JwtUtils.token_required
def upload_report(_dir, filename):
    report_root_dir = application.config['REPORT_ROOT_DIR']
    return send_from_directory(f"{report_root_dir}/{dir}/", filename)


@module_route.route(f'/{module_name}/QueryByPage', methods=["POST"])
# @JwtUtils.token_required
def query_api_history_by_page():
    try:
        page = int(request.json["page"])
        page_size = int(request.json["pageSize"])
        with application.app_context():
            # 分页查询
            filter_list = []
            # 添加 项目筛选条件
            collection_id = int(request.json.get("collection_id", 0))
            # 没有实现双条件查询
            if collection_id > 0:
                filter_list.append(module_model.collection_id == collection_id)
            # 添加模块名称搜索条件
            query_module_name = request.json.get("module_name", "")
            if query_module_name:
                filter_list.append(module_model.module_name.like(f'%{module_name}%'))

            datas, total = DbHandler.query_by_page_by_filters(module_model, filter_list, page, page_size)
            return RespModel.ok_resp(obj_list=datas, obj_list_key="data", dict_t={"total": total}, msg='查询api模块成功')

    except ValueError as e:
        return RespModel.error_resp(msg='query_api_history_by_page 参数错误')


@module_route.route(f'/{module_name}/QueryById', methods=["GET"])
# @JwtUtils.token_required
def query_api_history_by_id():
    try:
        req_args = request.args
        history_id = int(req_args.get('id'))
        with application.app_context():
            proj = DbHandler.query_by_id(module_model, history_id)
            if proj:
                return RespModel.ok_resp(obj_list=[proj], obj_list_key="data", msg='查询成功')
            else:
                return RespModel.ok_resp(msg='查询成功，数据为空')
    except ValueError as e:
        return RespModel.error_resp(msg='参数错误')


# @module_route.route(f'/{module_name}/CreateAction', methods=["POST"])
# @JwtUtils.token_required
# def create_api_history_action():
#     """
#     新增 api project
#     :return:
#     """
#     try:
#         with application.app_context():
#             pass
#             # request.json["id"] = None  # ID自增长
#             # data = module_model(**request.json, create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))
#             # db.session.add(data)
#             # # 获取新增后的ID并返回
#             # db.session.flush()
#             # data_id = data.id
#             # db.session.commit()
#         return RespModel.ok_resp(msg='添加成功', dict_t={'id': data_id})
#     except ValueError as e:
#         return RespModel.error_resp(msg='参数错误')


@module_route.route(f'/{module_name}/UpdateAction', methods=["PUT"])
@JwtUtils.token_required
def update_api_history_action():
    try:
        with application.app_context():
            pass
            # req_data = dict(request.json)
            # proj_id = req_data.get('id')
            # update_pro = module_model.query.filter_by(id=proj_id).first()
            # if update_pro:
            #     req_data.pop('id')
            #     [update_pro.__setattr__(k, req_data.get(k)) for k in req_data.keys()]
            #     db.session.commit()
            #     return RespModel.ok_resp(msg=f'项目{proj_id}修改成功')
            # else:
            #     return RespModel.error_resp(msg=f'项目id：{proj_id}不存在')
            # pass
    except ValueError as e:
        return RespModel.error_resp(msg='参数错误')


@module_route.route(f'/{module_name}/DeleteAction', methods=["DELETE"])
@JwtUtils.token_required
def delete_api_history_action():
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
