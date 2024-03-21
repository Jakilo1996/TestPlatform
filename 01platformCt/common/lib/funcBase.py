# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   acnsdpautotestv2
# FileName:     baseUtil.py
# Author:      Jakiro
# Datetime:    2023/1/31 17:27
# Description:  封装了一些基础帮助函数以及装饰器
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import time
import uuid
import traceback
from functools import reduce, wraps
from typing import Any, Optional, Callable, Type, Union, List, Dict, Tuple
from operator import methodcaller
from datetime import datetime

import signal
import threading


class MyDictLoopSet(dict):
    """
    类字典类，可以传入 k: 'k1,k2,k3' v :v1  递归赋值  {k1:{k2:{k3:v}}}
    """

    def __init__(self, *args, **kwargs):
        super(MyDictLoopSet, self).__init__(*args, **kwargs)

    def __setitem__(self, key: str, value):
        if '.' in key:
            keys = key.split('.', 1)
            child_dict = MyDictLoopSet()
            child_dict[keys[1]] = value
            super(MyDictLoopSet, self).__setitem__(keys[0], child_dict)
        else:
            super(MyDictLoopSet, self).__setitem__(key, value)


class DotDict(dict):
    """
    字典支持.key递归出所有value
    """

    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = DotDict(value)
        return value


class MyDictRecursionKeyValue(dict):
    """
    通过一次 key=value  将字典中所有嵌套字典的相同key改为value
    """

    def __init__(self, *args, **kwargs):
        super(MyDictRecursionKeyValue, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super(MyDictRecursionKeyValue, self).__setitem__(key, value)
        for k in self.keys():
            if isinstance(self[k], dict):
                dict2 = MyDictRecursionKeyValue(self[k])
                dict2.__setitem__(key, value)
                super(MyDictRecursionKeyValue, self).__setitem__(k, dict2)


class InstanceMethodParamCall:
    """
    声明一个类，这个类的子类，可以通过实例(method name)的方式，调用类中的方法
    """

    def get_methods(self) -> list:
        """
        # 获得当前类的所有方法名
        :return: 当前类的所有方法名
        """
        return (list(filter(lambda m: not m.startswith("_") and callable(getattr(self, m)),
                            dir(self))))

    def __call__(self, *args, **kwargs):
        method = kwargs.get('method')
        if method in self.get_methods():
            kwargs.pop('method')
            if kwargs:
                caller = methodcaller(method, *args, **kwargs)
            else:
                caller = methodcaller(method)

            return caller(self)
        else:
            print('不支持的项目类型')


def timeout_callback(e):
    raise e


def _timeout_callback():
    raise TimeoutError('超时回调')


class SupportFunc:
    InstanceMethodParamCall = InstanceMethodParamCall
    DotDict = DotDict
    MyDictRecursionKeyValue = MyDictRecursionKeyValue

    @staticmethod
    def call_func_decorator(prefix='') -> Callable:
        """
        声明一个装饰器方法，装饰函数，打印被装饰函数的执行时间
        :param prefix: 调试前缀
        :return: func的返回值
        """

        def dec(func: Callable) -> Callable:
            @wraps(func)
            def inner(*args, **kwargs):
                print(f'call {prefix}_{func.__name__}')
                start_time = time.time()
                reason = func(*args, **kwargs)
                end_time = time.time()
                print(f'{prefix}_{func.__name__} duration {(end_time - start_time):.3f}')
                return reason

            return inner

        return dec

    @staticmethod
    def object_param_call_method_decorator(_object: Type) -> Type:
        """
       装饰一个类，使这个类的实例，可以通过   实例(实例方法)   的形式调用实例的方法
       :return:类
       """

        def get_methods(_object: Type) -> list:
            """
            # 获得当前类的所有方法名
            :return: 当前类的所有方法名
            """
            return (list(filter(lambda m: not m.startswith("_") and callable(getattr(_object, m)),
                                dir(_object))))

        def call(self, *args, **kwargs):
            method = kwargs.get('method')
            if method in self.get_methods():
                kwargs.pop('method')
                if kwargs:
                    caller = methodcaller(method, *args, **kwargs)
                else:
                    caller = methodcaller(method)

                return caller(self)
            else:
                print(f'{_object.__name__}不支持的方法类型:{method}')

        _object.get_methods = get_methods
        _object.__call__ = call
        return _object

    @staticmethod
    def simple_instance_class_base_decorator(_class) -> Type:
        """
        装饰一个类，继承这个类的其他方法，返回这个类的单例类
        :param _class: 类
        :return: 类的单例类
        """

        class SimpleInstanceClass(_class):
            _instance = None

            def __new__(cls, *args, **kwargs) -> _instance:
                if not cls._instance:  #
                    cls._instance = super(_class, cls).__new__(cls)
                return cls._instance

        return SimpleInstanceClass

    @staticmethod
    def time_out_decorator(interval, callback=timeout_callback) -> Callable:
        """
        声明一个装饰器，传入超时时间，超时报错 使用方式 信号
        :param interval: 超时时间，仅linux有效
        :param  callback 回调函数
        :return:
        """

        def decorator(func: Callable):
            def handler(signum, frame):
                raise TimeoutError("run func timeout")

            def wrapper(*args, **kwargs):
                try:
                    signal.signal(signal.SIGALRM, handler)
                    signal.alarm(interval)  # interval秒后向进程发送SIGALRM信号
                    result = func(*args, **kwargs)
                    signal.alarm(0)  # 函数在规定时间执行完后关闭alarm闹钟
                    return result
                except TimeoutError as e:
                    callback(e)

            return wrapper

        return decorator

    @staticmethod
    def time_out_by_threading_decorator(interval, callback=_timeout_callback) -> Callable:
        """
        声明一个装饰器，传入超时时间，超时报错 使用方式 多线程
        :param interval: 超时时间
        :param callback: 函数调用
        :return:
        """

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                t = threading.Thread(target=func, args=args, kwargs=kwargs)
                t.setDaemon(True)  # 设置主线程结束 子线程立刻结束
                t.start()
                t.join(interval)  # 主线程阻塞等待interval秒
                if t.is_alive() and callback:
                    return threading.Timer(0, callback).start()  # 立即执行回调函数
                else:
                    return

            return wrapper

        return decorator

    @staticmethod
    def set_default(instance_, k, v):
        """
        传入一个实例，和实例的属性键值对，如果有这个属性，则不改变原有属性的值，如果没有，则为实例新增属性
        :param instance_: 实例
        :param k: 属性名
        :param v: 属性值
        :return:
        """
        try:
            getattr(instance_, k)
        except AttributeError:
            setattr(instance_, k, v)


# 自定义超时异常
class _TimeoutError(Exception):
    def __init__(self, msg):
        super(_TimeoutError, self).__init__()
        self.msg = msg


class BaseTools:
    @staticmethod
    def eval_str(str1: str) -> Any:
        """
        传入一个字符串格式的字典或列表、纯字符串，如果是字符串不做处理，如果是可转化类型，返回转换后的类型
        :param str1: 字符串格式的列表，字典
        :return: 转换后对应的python数据类型
        """
        reason = None
        try:
            reason = eval(str1)
        except NameError:
            reason = str1
        finally:
            return reason

    @staticmethod
    def get_attr(obj: object, ignore_keys: Optional[list] = None) -> dict:
        """
        :param obj: 对象
        :param ignore_keys 不返回的 keys列表
        :return: 返回对象的所有非私有属性字典
        """
        custom_attributes = dict()
        attr = vars(obj)

        for att, value in attr.items():
            if not att.startswith('__') and not att.startswith('_') and not callable(value):
                custom_attributes[att] = value
        if ignore_keys:
            for k in ignore_keys:
                if k in custom_attributes.keys():
                    del custom_attributes[k]
        return custom_attributes

    @staticmethod
    def generate_uuid() -> str:
        return uuid.uuid4().__str__()


class ExceptionBase:
    @staticmethod
    def catch_exceptions_callback(call_back: Callable[[Exception, str], Any],
                                  e_tuple: Tuple[Type[Exception]] = (Exception,)) -> Callable:
        """
        它用于捕获特定类型的异常，并调用一个回调函数进行处理。
        打印了代码所在行数，用于平台内部的运行。
        :param call_back: 这是一个回调函数，它接受两个参数：异常对象和异常消息。它负责处理捕获到的异常。
        :param e_tuple: 这是一个元组，其中包含了要捕获的异常类型。默认情况下，它捕获所有的异常类型（Exception）
        :return:Callable
        """

        def catch_exceptions(func):
            """
            catch_exceptions 装饰器函数将目标函数包装在内部的 wrapper 函数中。
            :param func:
            :return:
            """

            @wraps(func)
            def wrapper(*args, **kwargs):
                """
                在 wrapper 函数中，它使用 try-except 块来捕获指定类型的异常。
            如果捕获到了异常，则会调用 call_back 回调函数，并传递异常对象和相应的错误消息。
                :param args:
                :param kwargs:
                :return:
                """
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # 获取异常发生的行数
                    tb_info = traceback.extract_tb(e.__traceback__)
                    line_number = tb_info[-1].lineno
                    filename = traceback.extract_tb(e.__traceback__)[-1].filename
                    if isinstance(e, e_tuple):
                        err_msg = f"{e.__class__.__name__} File:'{filename}  'Function '{func.__name__}' encountered an exception at line {line_number}: {e}"
                        call_back(e, err_msg)
                        # 这里可以根据需求进行更多的异常处理操作，如记录日志、发送警报等
                        # raise  # 如果希望继续抛出异常，则需要添加这一行
                    else:
                        # 在 else 分支中创建新的异常，并将原始异常作为其原因
                        err_msg = f"Function '{func.__name__}'e_tuple中未处理的异常： encountered an exception at line {line_number}: {e}"
                        call_back(e, err_msg)
                        err = Exception(err_msg)

                        raise err from e

            return wrapper

        return catch_exceptions


if __name__ == '__main__':
    def call_back_func(e, e_str):
        print(e.__dict__)
        print(e.__class__.__name__, e_str)
        # err = Exception()
        pass


    @ExceptionBase.catch_exceptions_callback(call_back_func, (KeyError,))
    def a(b_dict, k):
        return b_dict[k]


    d_dict = {'a': 1}
    a(d_dict, 'b')
