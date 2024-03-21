# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     dbHandler.py
# Author:      Jakilo
# Datetime:    2024/2/23 14:49
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description: 处理数据库事务以及非事务的查询操作
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

from typing import Optional, Type, List, Dict, TypeVar, Union

from flask_sqlalchemy.query import Query
from flask_sqlalchemy.model import Model

from app import application, db
from common.lib.funcBase import BaseTools

TModelSubclass = TypeVar('TModelSubclass', bound=Model)
TDbModelSubClass = TypeVar('TDbModelSubClass', bound=db.Model)


def query_by_filters(module_model: Type[Model], filter_list: List[bool]) -> Optional[
    Query]:
    """
    根据筛选条件，对Model 进行筛选，返回 Query 对象
    :param module_model: 进行筛选的 model
    :param filter_list: 筛选条件列表
    :return:
    """
    return module_model.query.filter(*filter_list)


def query_by_filter_by(module_model: Type[Model], **kwargs) -> Optional[Query]:
    # 获取模型的所有属性名
    columns = module_model.__table__.columns.keys()
    # 构建过滤条件
    filters = {}
    for key, value in kwargs.items():
        # 只选择模型中存在的属性名作为过滤条件
        if key in columns:
            filters[key] = value
        # 使用 filter_by 方法进行过滤
    return module_model.query.filter_by(**filters)


def paging_query(query: [Query], page: int, page_size: int) -> (Optional[List[Model]], int):
    """
    将返回的 query 对象进行分页操作，返回分页后的返回内容 以及分页统计
    :param query:
    :param page:
    :param page_size:
    :return:
    """
    return query.limit(page_size).offset((page - 1) * page_size).all(), query.count()


class DbHandler:
    @staticmethod
    def query_by_filter_by_all(module_model: Type[Model], **kwargs):
        return query_by_filter_by(module_model, **kwargs).all()

    @staticmethod
    def query_by_filter_by_first(module_model: Type[Model], **kwargs):
        return query_by_filter_by(module_model, **kwargs).first()

    @staticmethod
    def query_by_page_by_filters(module_model: Type[TModelSubclass], filter_list: list, page: int, page_size: int) -> (
            Optional[List[Type[TModelSubclass]]], int):
        """
        通过筛选条件，筛选模型符合条件的数据，并分页返回，适用于支持筛选并分页返回的视图函数
        :param module_model: Type[TModelSubclass]
        :param filter_list:
        :param page:
        :param page_size:
        :return:
        """
        query = query_by_filters(module_model, filter_list)
        return paging_query(query, page, page_size)

    @staticmethod
    def query_by_page_only(module_model: Type[TModelSubclass], page: int, page_size: int) -> (
            Optional[List[Model]], int):
        """
        对模型的结果进行分页，适用于需要分页返回的视图函数
        :param module_model: Type[TModelSubclass]
        :param page:
        :param page_size:
        :return:
        """
        return paging_query(module_model.query, page, page_size)

    @staticmethod
    def query_by_filters_only(module_model: Type[TModelSubclass], filter_list: list) -> (Optional[List[Model]], int):
        """
        对模型进行筛选，返回符合筛选条件的所有数据
        :param module_model: Type[TModelSubclass]
        :param filter_list:
        :return:
        """
        return query_by_filters(module_model, filter_list)

    @staticmethod
    def query_all(module_model: Type[TModelSubclass]) -> Optional[List[Model]]:
        """
        返回全部的模型数据列表
        :param module_model:
        :return:
        """
        return module_model.query.all()

    @staticmethod
    def query_by_id(module_model: db.Model, _id: int) -> Optional[Model]:
        """
        根据 id 对模型进行筛选，id 需要为主键，仅返回一个数据
        :param module_model:
        :param _id:
        :return:
        """
        filter_list = [module_model.id == _id]
        return query_by_filters(module_model, filter_list).first()

    @staticmethod
    def update_action_by_id(module_model: db.Model, update_context: dict) -> bool:
        if 'id' in update_context.keys():
            filter_list = [module_model.id == update_context.pop('id')]
            # TODO 修改时间 需要更新所有模型的字段 update_time
            # {'update_time': datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')}
            update_data: Optional[Model] = query_by_filters(module_model, filter_list).first()
            if update_data:
                [update_data.__setattr__(k, update_context.get(k)) for k in update_context.keys()]
                db.session.commit()
                return True
        return False

    @staticmethod
    def delete_by_id_action(module_model: db.Model, _id: int) -> bool:
        filter_list = [module_model.id == _id]
        del_data: Optional[Model] = query_by_filters(module_model, filter_list).first()
        if del_data:
            db.session.delete(del_data)
            db.session.commit()
            return True
        else:
            return False

    @staticmethod
    def create_action(module_model: db.Model, create_context: dict) -> int:
        if 'id' in create_context.keys():
            create_context.pop('id')
        create_context.update({'create_time': BaseTools.generate_current_strf_time()})
        create_data = module_model(**create_context)
        db.session.add(create_data)
        # 获得自增的 id 并返回
        db.session.flush()
        create_data_id = create_data.id
        db.session.commit()
        return create_data_id
