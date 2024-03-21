# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     JwtUtil.py
# Author:      Jakiro
# Datetime:    2024/1/10 15:49
# Description:
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Callable, Dict

import jwt
from flask import request

from app import application
from web.utils.respUtil import http_response, RespModel

# 存储 Token 的过期时间戳
_expired_tokens: Dict[str, datetime] = dict()  # { token_str: expired_time,}
_tokens: Dict[str, str] = dict()  # { token_str: user_id，}


def clean_expired_tokens_crontab():
    """
    定期清理 过期的token
    :return:
    """
    current_time = datetime.utcnow()
    _expired_tokens_copy = _expired_tokens.copy()
    for token_str, expired_time in _expired_tokens_copy.items():
        if expired_time <= current_time:
            del _expired_tokens[token_str]  # 从过期时间戳字典中移除过期的 token,del 字典内部使用哈希表实现，速度较快
            del _tokens[token_str]  # 从有效 token字典中移除过期 token
            print(f'clean token_str :{token_str} by scheduled task')
    print(f'clean_expired_tokens scheduled task finish')


def create_token_str(create_payload, key: str) -> str:
    """
    生成 token_str
    :param create_payload:
    :param key:
    :return:
    """
    return jwt.encode(payload=create_payload, key=key, algorithm='HS256')


def decode_token(_token_str: str, key: str) -> Optional[dict]:
    """
    解密 token
    :param _token_str:
    :param key:
    :return: Optional[dict]
    """
    try:
        _payload = jwt.decode(jwt=_token_str, key=key, algorithms=['HS256'])

        return _payload

    except jwt.InvalidTokenError:
        application.logger.info('无法校验的 token')
        return


def update_token_expiration_date():
    """
    返回当前时间的 30分钟后
    :return:
    """
    return datetime.utcnow() + timedelta(minutes=300)


def create_token(username: str, user_id: str) -> str:
    """
    通过用户名和用户 id加密生成 token,返回 token
    :param username: 用户名
    :param user_id: 用户 id
    :return: str
    """
    # 拿出配置的 key
    key = application.config.get('SECRET_KEY')
    # 获得当前生成 token 的过期时间
    _token_expiration_date = update_token_expiration_date()
    # 要把什么内容换成 Token
    payload_ = {
        'username': username,
        'user_id': user_id,
        'exp': _token_expiration_date
    }
    token_str = create_token_str(create_payload=payload_, key=key)
    _tokens.update({token_str: user_id})
    return token_str


def del_token_by_user_id(user_id: str) -> bool:
    """
    根据用户 id 删除 token
    :param user_id:
    :return:
    """
    for k, v in _tokens.items():
        if v == user_id:
            del _tokens[k]
            return True  # 找到第一个符合的对象，停止遍历
    return False


def del_token_by_token_str(token_str: str) -> bool:
    """
    通过 token_str 删除 token
    :param token_str: token_str
    :return:
    """
    if token_str in _tokens.keys():
        del _tokens[token_str]
        return True
    return False


class JwtUtils(object):
    @staticmethod
    def login_token_action(username: str, user_id: str) -> str:
        """
        通过用户名和用户 id，验证当前用户是否有有效的 token，如果有，将原来的 token 失效，并返回新 token，如果没有，返回新 token
        :param username: 用户名
        :param user_id:  用户 id
        :return: token_str
        """
        if user_id in _tokens.values():
            del_token_by_user_id(user_id)
        # print(username)
        token_str = create_token(username, user_id)
        return token_str

    @staticmethod
    def logout_token_action(token_str: str) -> bool:
        return del_token_by_token_str(token_str)

    @staticmethod
    def token_required(f: Callable) -> Callable:
        """
        装饰视图函数，视图函数需要检查Authorization请求头的 token 是否有效，
        如果有效，则可以正常执行视图函数，并更新 token 的有效时长，
        如果token过期，则清除 token 信息，返回Token is missing or expired，201
        如果 token无效，返回 Token is missing or expired，201
        :param f: ViewFunc
        :return:HttpResp
        """

        @wraps(f)
        def inner_func(*args, **kwargs):
            tag = application.config.get('TOKEN_REQUIRED')
            if tag:
                headers = request.headers
                token_str = headers.get('Authorization', None)
                data = {
                    'redirect': r'/login',
                    "message": "Token is missing or expired"
                }
                if token_str in _tokens.keys():
                    # 拿出配置的 key
                    _key = application.config.get('SECRET_KEY')

                    try:
                        _payload = decode_token(token_str, _key)
                        if _payload:
                            # application.logger.info(f'verify token_str :{token_str}')
                            return f(*args, **kwargs)
                        else:
                            if del_token_by_token_str(token_str):
                                application.logger.info(f'clean token_str :{token_str}')

                    except Exception as e:
                        application.logger.error(f'Error verify_token_decorator {f.__name__}:{e}')
                        return RespModel.internal_server_error_resp(e)
                return http_response(status=201, headers={}, data=data)
            else:
                return f(*args, **kwargs)
        return inner_func


if __name__ == '__main__':
    token_expiration_date = datetime.utcnow() + timedelta(days=7)

    token = create_token('admin', '1')
    # 400 参数错误 401 用户认证美国  403 没权限 404没找到 405 方法不支持

    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6IjEiLCJleHAiOjE3MDg0ODUwNzR9.FC4uXG7PmAZX-kikcI2X2h5w3p5q-547i_MI8kWqPFM'
    payload = decode_token(token, 'llx111122223333')
    print(payload)
    print(datetime.utcfromtimestamp(payload['exp']))
    # print(verify_token(
    #     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJhZG1pbiIsImV4cCI6MTcwODI0MzIzNX0.eLgFPG1S6H_Tvrkk0SV-UN5VjK6WWqzLjRPNE19S2q4',
    #     'llx111122223333'))
