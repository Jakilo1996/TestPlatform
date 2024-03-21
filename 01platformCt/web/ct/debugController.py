# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     debugController.py
# Author:      Jakilo
# Datetime:    2024/1/17 17:03
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则 目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import datetime

from typing import Union, Type

from flask import Blueprint, request
from flask_sqlalchemy.query import Query
# from flask_sqlalchemy.model import Model

import app
from common.modules.sys_manage.user import User
# from web.utils.JwtUtil import JwtUtils
from web.utils.respUtil import RespModel

module_model=User
# 生成蓝图
route_debug = Blueprint('debug_page', __name__)


@route_debug.route('/debug', methods=['GET'])
def debug_action():
    req_args = request.args
    del_user_id = req_args.get('id')
    if del_user_id:

        del_user: Union[Query, None] = module_model.query.filter_by(id=del_user_id).first()
        1/0
        if del_user:
            app.db.session.delete(del_user)
            app.db.session.commit()
            return RespModel.ok_resp(msg=f'用户{del_user_id}删除成功')
        else:
            return RespModel.error_resp(msg=f'用户{del_user_id}未找到')

    else:
        return RespModel.error_resp(msg='id 参数错误')