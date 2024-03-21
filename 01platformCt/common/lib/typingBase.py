# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     typingHelper.py
# Author:      Jakilo
# Datetime:    2024/3/13 15:15
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description: 需要使用的类型的声明方法，为保证代码清晰，不导入
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from typing import Optional  # 表示可选类型，可以是指定的类型或 None。
from typing import Union  # 表示联合类型，可以是指定的多个类型中的任意一个。
from typing import Any  # 表示任意类型。
from typing import Callable  # 表示可调用对象的类型，如函数。
from typing import ClassVar  # 用于指示类变量的类型，表示类级别的变量，属于整个类，不属于类的实例
from typing import Generic  # 表示泛型类型。
from typing import Tuple  # 表示元祖类型
from typing import Type  # 表示类型对象的类型。
from typing import TypeVar  # 表示类型变量，通常用于泛型编程中
from typing import List  # 表示列表类型
from typing import Dict  # 表示字典类型
from typing import Set  # 表示集合类型
from typing import ForwardRef  # 表示对类型的前向引用，通常用于在类型注释中引用尚未定义的类。

# 假设字典的键值对类型分别为 str 和 int
ListOfDictsStrInt = List[Dict[str, int]]
# 假设字典的键值对类型分别为 str 和 str
ListOfDictsStrStr = List[Dict[str, str]]

# 元祖，第一个元素是 bool，第二个元素是字典或者字符串
TupleOfBoolUnionDictStr = Tuple[bool, Union[dict, str]]


class MyClass:
    count: ClassVar[int] = 0  # 类变量 count，类型为整数

    def __init__(self, name: str) -> None:
        self.name = name
        MyClass.count += 1


T = TypeVar("T")


def process_items(items: List[T]) -> None:
    for item in items:
        print(item)


T = TypeVar("T")


class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item


# 创建一个包含不同类型数据的盒子
box1 = Box(10)
box2 = Box("Hello")
box3 = Box([1, 2, 3])

# 在类型注释中引用尚未定义的类
Node = ForwardRef("Node")


class Node:
    def __init__(self, value: int, next_node: "Node" = None) -> None:
        self.value = value
        self.next_node = next_node
