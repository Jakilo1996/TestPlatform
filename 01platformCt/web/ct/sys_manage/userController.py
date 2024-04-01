# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     userController.py
# Author:      Jakiro
# Datetime:    2024/1/15 18:18
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from datetime import datetime
from typing import Union, Type

import pymysql
from flask import Blueprint, request
from flask_sqlalchemy.query import Query

from app import db, application
from common.modules.sys_manage.user import User
from web.utils.respUtil import RespModel
from web.utils.jwtUtil import JwtUtils
from web.utils.dbHandler import DbHandler

# 生成蓝图
module_name = "CtApiUser"  # 模块名称
module_model: Type[User] = User
module_route = Blueprint(f"route_{module_name}", __name__)

# 定义用户列表查询接口
'''
1. 前端给出查询条件，当前的页数，和每页的长度，
2. 接口返回当前显示数据，以及数据的长度
'''


@module_route.route(f'/{module_name}/GetList', methods=['GET'])
@JwtUtils.token_required
def get_user_list():
    req_args = request.args  # get参数的获取方式
    # app.app.logger.info('in getUserLisr')
    try:
        page_size = int(req_args.get('per_page'))
        page = int(req_args.get('current_page'))

        if page_size and page:
            if page_size >= 0 and page >= 0:
                with application.app_context():
                    t_dict = dict()

                    user_data, t_dict['total'] = DbHandler.query_by_page_only(module_model, page, page_size)
                    return RespModel.ok_resp(obj_list=user_data, obj_list_key='user_data', msg='查询成功',
                                             dict_t=t_dict, ignore_keys=['token'])
                    # else:
                    #     return RespModel.error_resp(msg='查询失败，不支持超过查询长度限制错误')
            else:
                return RespModel.error_resp(msg='查询失败，传入的查询条件为负数')
        else:
            return RespModel.error_resp(msg='per_page or currentPage 参数错误')
    except ValueError as e:
        application.logger.error(f'ct_get_user_list {e}')
        return RespModel.error_resp(msg='per_page or current_page 参数类型错误')


@module_route.route(f'/{module_name}/CreateAction', methods=['POST'])
@JwtUtils.token_required
def create_usr_action():
    req_json = request.json  # post 参数的获取方式
    username = req_json.get('username')
    password = req_json.get('password')
    role = req_json.get('role')
    print(request.cookies)
    # 需要检查创建用户的权限
    if username and password and role:
        with application.app_context():
            new_user: User = module_model(username=username, password=password, role=role,
                                          create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))

            db.session.add(new_user)
            db.session.commit()
        return RespModel.ok_resp(obj=new_user, msg=f'创建{username}用户成功')

    else:
        return RespModel.error_resp(msg=f'create_usr_action 参数错误')


@module_route.route(f'/{module_name}/DeleteAction', methods=['DELETE'])
@JwtUtils.token_required
def delete_user_action():
    try:
        with application.app_context():
            req_args = request.args
            del_user_id = int(req_args.get('id'))
            if del_user_id:

                del_user = DbHandler.delete_by_id_action(module_model, del_user_id)
                if del_user:
                    db.session.delete(del_user)
                    db.session.commit()
                    return RespModel.ok_resp(msg=f'用户{del_user_id}删除成功')
                else:
                    return RespModel.error_resp(msg=f'用户{del_user_id}未找到')
            else:
                return RespModel.error_resp(msg='delete_user_action id 参数错误')
    except ValueError as e:
        return RespModel.error_resp(msg='delete_user_action id 参数类型错误')


@module_route.route(f'/{module_name}/UpdateAction', methods=['PUT'])
@JwtUtils.token_required
def update_user_action():
    req_json = request.json  # post 参数的获取方式
    update_user_id = req_json.get('id')
    with application.app_context():
        update_user: Union[User, None] = module_model.query.filter_by(id=update_user_id).first()
        if update_user:
            update_user_info = ['username', 'password', 'role']
            update_user_info_dict = {k: req_json.get(k) for k in update_user_info}
            [update_user.__setattr__(k, update_user_info_dict.get(k)) for k in update_user_info_dict.keys() if
             update_user_info_dict.get(k)]
            db.session.commit()
            return RespModel.ok_resp(msg=f'用户{update_user_id}修改成功')

        else:
            return RespModel.error_resp(msg=f'update_user_action 用户{update_user_id}未找到')
