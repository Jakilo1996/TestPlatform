# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     respModel.py
# Author:      Jakiro
# Datetime:    2024/1/10 16:47
# Description:
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from typing import Optional

from flask import jsonify, Response

from common.lib.funcBase import BaseTools
from app import application


def http_response(headers: Optional[dict] = None, status: int = 200, data: Optional[dict] = None) -> Response:
    """
    # # 400 参数错误 401 用户认证不通过  403 没权限 404没找到 405 方法不支持
    # 406 Not Acceptable：客户端请求的格式不可接受，通常是因为请求的内容类型不符合服务器的要求。
    409 Conflict：服务器无法处理请求，因为存在冲突，通常是因为请求的操作与资源的当前状态冲突。
    410 Gone：请求的资源已经不存在，服务器永久性地禁止对资源的访问。
    429 Too Many Requests：客户端发送的请求过于频繁，超出了服务器的请求限制。

    500 服务器错误  504 时间超时
    :param headers:
    :param status:
    :param data:
    :return:
    """
    _data = {"message": " "}

    if data:
        _data = data
    resp = jsonify(_data)
    if headers:
        resp.headers.update(headers)
    resp.status = status
    return resp


class RespModel:
    @staticmethod
    def ok_resp(obj: object = None, msg: str = None, obj_list: [object] = None, obj_list_key: Optional[str] = None,
                dict_t: dict = None, ignore_keys: list = None) -> Response:
        """
        请求成功的返回基础定义
        :param obj: 需要返回的对象信息
        :param msg: 需要返回的提示信息
        :param obj_list: 传入的列表对象
        :param obj_list_key 传入列表对象返回的 key
        :param dict_t: 额外需要传回的信息
        :param ignore_keys 不需要返回的实例属性
        :return: 类 resp 的字典对象
        """
        resp = dict()
        resp['msg'] = msg
        obj_list_data = []
        dic = dict()

        if obj:
            dic.update(BaseTools.get_attr(obj, ignore_keys))
        if obj_list_key:
            for per_obj in obj_list:
                obj_list_data.append(BaseTools.get_attr(per_obj, ignore_keys))
            dic.update({obj_list_key: obj_list_data})
        if dict_t:
            dic.update(dict_t)
        if dic:
            resp['data'] = dic

        return http_response(data=resp, status=200)

    @staticmethod
    def ok_resp_simple_list(lst: Optional[list] = None, msg: Optional[str] = None, total: int = 0) -> Response:
        resp = dict()
        dic = dict()
        dic['data'] = lst
        dic['total'] = total
        resp['data'] = dic
        resp['msg'] = msg
        return http_response(data=resp, status=200)

    @staticmethod
    def error_resp(msg: str) -> Response:
        """
        请求失败的返回基础定义
        :param msg:返回的失败信息
        :return: 类 resp 的字典对象
        """
        resp = dict()
        resp['message'] = msg
        return http_response(data=resp, status=400)

    @staticmethod
    def internal_server_error_resp(error: Exception) -> Response:
        """
        记录服务器内部错误日志
        :param error:报错类
        :return: 返回500 并返回服务器内部错误信息
        """

        application.logger.error(error)
        error_response = {
            "error": "internal_server_error_resp 发生异常",
            "message": '服务器内部错误,操作失败'
        }
        return http_response(data=error_response, status=500)


# 使用@app.errorhandler装饰器定义全局错误处理方法
@application.errorhandler(Exception)
def handle_error(error):
    # 捕获异常并返回自定义的错误响应
    application.logger.error(error)
    error_response = {
        "error": "发生异常",
        "message": '服务器内部错误,操作失败'
    }
    return jsonify(error_response), 500  # 返回JSON格式的错误响应和HTTP状态码
