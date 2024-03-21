# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   acnsdpautotestv2
# FileName:     baseTools.py
# Author:      Jakiro
# Datetime:    2023/1/31 17:27
# Description:  封装了一些基础帮助函数以及装饰器
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import json
import time
import signal
import threading
from functools import reduce
from operator import methodcaller
from datetime import datetime

from typing import Any

from functools import wraps

from jsonpath import jsonpath


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


class InstanceMethodParamCall():
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


class SupportFunc():
    InstanceMethodParamCall = InstanceMethodParamCall
    DotDict = DotDict
    MyDictRecursionKeyValue = MyDictRecursionKeyValue

    @staticmethod
    def call_func_decorator(prefix=''):
        """
        声明一个装饰器方法，装饰函数，打印被装饰函数的执行时间
        :param prefix: 调试前缀
        :return: func的返回值
        """

        def dec(func):
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
    def object_param_call_method_decorator(_object):
        """
       装饰一个类，使这个类的实例，可以通过   实例(实例方法)   的形式调用实例的方法
       :return:类
       """

        def get_methods(_object) -> list:
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
    def simple_instance_class_base_decorator(_class):
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
    def time_out_decorator(interval, callback=timeout_callback):
        """
         声明一个装饰器，传入超时时间，超时报错 使用方式 信号
        :param interval: 超时时间，仅linux有效
        :param callback: 超时调用的函数
        :return:
        """

        def decorator(func):
            def handler(signum, frame):
                raise _TimeoutError("run func timeout")

            def wrapper(*args, **kwargs):
                try:
                    signal.signal(signal.SIGALRM, handler)
                    signal.alarm(interval)  # interval秒后向进程发送SIGALRM信号
                    result = func(*args, **kwargs)
                    signal.alarm(0)  # 函数在规定时间执行完后关闭alarm闹钟
                    return result
                except _TimeoutError as e:
                    callback(e)

            return wrapper

        return decorator

    @staticmethod
    def time_out_by_threading_decorator(interval, callback=_timeout_callback):
        """
        声明一个装饰器，传入超时时间，超时报错 使用方式 多线程
        :param interval: 超时时间
        :param callback: 函数调用
        :return:
        """

        def decorator(func):
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


class SupportTest:
    @staticmethod
    def json_path_v2(object_: object, expr: str):
        """
        :param object_: 一个待提取的json返回值；1：json字符串 response.json()返回值 2；被mysql类处理过的对象，期望是一个字典
        :param expr: 传入一个JsonPath表达式
        :return: 如果expr 无法提取出对应的value 则抛出ValueError；如果对应的object 不属于可以JsonPath的格式，则抛出ValueError
        如果expr 提取的值仅能返回一个数据，则返回数据 object，如果返回多组数据，则返回列表 list
        """
        reason = jsonpath(object_, expr)
        if not reason:
            raise ValueError(f'JsonPath 不能提取到结果,表达式:{expr},抽取对象{object_}')
        elif len(reason) == 1:
            return reason[0]
        else:
            return reason

    @staticmethod
    def eval_str_to_json(data: Any) -> str:
        """
        传入任何格式，如果是一个可以转义为python类型的字符串，将其序列化成json字符串，如果已经是字典或列表，则直接序列化成json
        :param data:
        :return:
        """
        if isinstance(data, str):
            return json.dumps(eval_str(data))
        elif isinstance(data, (dict, list)):
            return json.dumps(data)

    @staticmethod
    # 声明一个报错处理装饰器，装饰一个类，指定一种报错类型，如果出现此类报错类型，则进行log打印
    def assert_ec_decorator(error_msg_template: str, success_msg_template: str, ec: Exception = AssertionError):
        """

        :param error_msg_template: 报错的模版：需要留下4个可format的位置
        :param success_msg_template: 成功的模版，需要留下两个可format的位置
        :param ec: 捕获函数执行的报错类型
        :return: assert_func
        """

        def inner(func):
            """
            :param func: 断言函数
            :return:
            """

            @wraps(func)
            def call(*args, **kwargs):
                log = kwargs.get('log')
                expected = kwargs.get('assert_option').get('expected')
                actual = kwargs.get('actual')
                if not log:
                    raise ValueError('assert method has no log')
                try:
                    func(*args, **kwargs)
                except ec:
                    log.error(
                        f'AssertError {func.__name__} method {error_msg_template.format(expected, actual, expected, actual)}')
                    raise
                except Exception as e:
                    log.error(f'{func.__name__} method raise {e.__name__}')

                    raise
                else:
                    log.info(
                        f'AssertSuccess {func.__name__} ,{success_msg_template.format(expected, actual)}')

            return call

        return inner

    @staticmethod
    def current_time() -> list:
        """
        声明一个函数，用来生成当前时间，并返回两个数
        :return:第一个为 year-month-day 第二个为 hour-min
        """
        return list(map(lambda i: reduce(lambda x, y: str(x) + '-' + str(y), i), list(
            map(lambda i: [eval(f"datetime.now().{x}") for x in i], [('year', 'month', 'day'), ('hour', 'minute')]))))


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
