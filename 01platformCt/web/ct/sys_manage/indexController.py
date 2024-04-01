# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     indexController.py
# Author:      Jakiro
# Datetime:    2024/1/9 20:49
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

from flask import Blueprint, request
from sqlalchemy.orm.query import Query

from common.modules.sys_manage.user import User
from web.utils.jwtUtil import JwtUtils
from web.utils.respUtil import RespModel
from web.utils.dbHandler import DbHandler
from app import application, db

# 模块信息

module_model = User
module_route = Blueprint(f"route_login", __name__)


# 生成蓝图


@module_route.route('/')
def index():
    return 'HelloWorld!'


# 定义登录接口
'''
1. flask 有没有接口去接收请求，我规定 vue 到底发送什么东西给我
2. 前端应该传递什么参数 --- 用户名、密码
3. 跨域问题 前后端分离项目的跨域请求，请求地址对 CORS 跨域问题
4. 前端代码还缺少什么 --- 为什么要登录
5. 登录令牌 -- token 记录用户登录信息
6. 后续接口需要校验这个 token 是否是正确的令牌(是否能够解密回来？解密之后怎么知道用户名密码是不是登录成功的那个？)
'''


@module_route.route('/CtApiLogin', methods=['POST'])
def ct_login():
    """
    拿到用户名和密码查数据库，怎么确定账号密码是不是对的
    req_data: user_name,password
    查数据库的查询结果长度是否大于 1
    :return:
    """
    try:
        with application.app_context():
            req_json = request.json  # post 参数的获取方式
            username = req_json.get('username')
            password = req_json.get('password')
            filter_list = [module_model.username == username, module_model.password == password]
            user: Query = DbHandler.query_by_filters_only(module_model, filter_list).first()
            if user:
                t_dict = dict()
                try:
                    token_str = JwtUtils.login_token_action(username, str(user.id))
                    t_dict['token'] = token_str

                except Exception as e:
                    application.logger.error(f"ct_login {e}")
                return RespModel.ok_resp(obj=user, msg='登录成功', dict_t=t_dict, ignore_keys=['password'])
            else:
                return RespModel.error_resp(msg='登录失败，账号或密码错误')
    except ValueError as e:
        return RespModel.error_resp(msg='ct_login 参数错误')


@module_route.route('/CtApiLogout', methods=['POST'])
def ct_logout():
    """
    req_data: token_str
    :return:
    """
    req_json: dict = request.json
    token_str = req_json.get("ct-token")
    JwtUtils.logout_token_action(token_str)
    return RespModel.ok_resp(msg="登出成功")
