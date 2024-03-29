# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     pathUtil.py
# Author:      Jakilo
# Datetime:    2024/3/1 17:58
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------


import sys
import os
import shutil

from typing import Union


def get_base_proj_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def platform_path(path: str) -> str:
    if sys.platform == 'darwin' or sys.platform == 'linux':
        return path
    elif sys.platform == 'win32':
        return path.replace('/', '\\')


def normalized_path(path: str) -> str:
    """
    将路径中的斜杠统一为当前操作系统的斜杠符号（在Windows上为反斜杠\，在Unix/Linux上为斜杠/）。
    :param path:
    :return:
    """
    return os.path.normpath(path)


class PathOperation:

    def __init__(self):
        self._base_path = get_base_proj_dir()

    @staticmethod
    def path_join(first_path, second_path):
        return os.path.join(first_path, second_path)

    @staticmethod
    def make_dirs(path: str) -> None:
        """
        创建文件，忽略文件已存在时的报错
        :param path:
        :return:
        """
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def rm_tree(dir_path: str):
        shutil.rmtree(dir_path)

    @staticmethod
    def rm_dir(dir_path: str):
        os.rmdir(dir_path)

    @staticmethod
    def platform_path(path: str) -> str:
        """
        如果windows文件目录,将linux目录转换为windows目录
        :param path:
        :return:
        """
        return platform_path(path)

    @staticmethod
    def verify_path(path: str) -> str:
        """
        声明一个函数，传入一个目录或者文件路径。如果不存在，就报错;如果存在，显示验证正确
        :param path:
        :return:
        """
        if not os.path.exists(path):
            raise ValueError(f'{path}文件路径不存在')
        return path

    @staticmethod
    def make_dir_or_file(path):
        def is_exist(dir_p):
            if os.path.exists(dir_p):
                return True
            else:
                return False

        if '.' in path:
            if os.path.isfile(path):
                # 判断文件是否存在
                return path
            else:
                if not is_exist(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                    # 目录存在，则直接创建文件
                with open(path, 'w') as fp:
                    fp.close()
        else:
            if not is_exist(os.path.dirname(path)):
                os.makedirs(path)
        return path

    def make_dir_or_file_proj(self, path: str) -> str:
        """
        # 声明一个函数，传入一个项目根目录下的目录或者文件路经，如果存在 就返回这个路径，如果不存在，就循环创建这个目录以及文件 并返回path
        :param path: 路径
        :return:path
        """
        path = self.proj_path(path)

        def is_exist(dir_p):
            if os.path.exists(dir_p):
                return True
            else:
                return False

        if '.' in path:
            if os.path.isfile(path):
                # 判断文件是否存在
                return path
            else:
                if not is_exist(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                    # 目录存在，则直接创建文件
                with open(path, 'w') as fp:
                    fp.close()
        else:
            if not is_exist(os.path.dirname(path)):
                os.makedirs(path)
        return path

    @property
    def base_path(self) -> str:
        """
        找到项目的根目录
        :return:
        """
        return self._base_path

    def proj_workspace(self, proj: str) -> tuple:
        """
        传入参数名称，返回工作目录路径
        :param proj:
        :return:
        """
        data_path = self.base_path + f'/data/{proj}_proj'
        result_path = self.base_path + f'/result/{proj}_proj'
        return data_path, result_path

    def copy_file(self, source_file: str, target_dir: str) -> str:
        """
        传入源文件路径，将文件保存到新路径
        :param source_file:
        :param target_dir:
        :return:
        """
        try:
            shutil.copy(self.base_path + source_file, self.base_path + target_dir)
            return target_dir
        except IOError as e:
            raise e
        except Exception:
            raise ("Unexpected error", sys.exc_info())

    def proj_local_debug_workspace(self, proj: str) -> str:
        return self.base_path + f'/local_debug/{proj}_proj/'

    def proj_path(self, path) -> str:
        return self.platform_path(self._base_path + "/" + path)

    def proj_path_join(self, first_path, second_path) -> str:
        return self.platform_path(self._base_path + "/" + first_path + "/" + second_path)

    def ls_all_file_by_type(self, path: str, file_extension: Union[str, bool] = None) -> list:
        """
        根据文件后缀名，筛选出所有符合要求的文件，返回文件列表
        :param path:
        :param file_extension: 文件后缀名
        :return:
        """
        # 扫描 文件夹下的指定 type
        suite_folder = self.proj_path(path)

        print(suite_folder)
        if file_extension:
            file_names = [(int(f.split("_")[0]), f) for f in os.listdir(suite_folder) if
                          f.endswith(f".{file_extension}") and f.split("_")[0].isdigit()]
            file_names.sort()
            file_names = [f[-1] for f in file_names]
            return file_names
        else:
            file_names = os.listdir(suite_folder)
            file_names.sort()
            return file_names

    # 构建目标文件夹路径
    @staticmethod
    def build_target_folder_path(target_date):
        return target_date.strftime("%Y-%m-%d")

    # 遍历目标文件夹下所有文件，返回
    @staticmethod
    def traverse_folder(log_folder):
        for root, dirs, files in os.walk(log_folder):
            for file in files:
                file_path = os.join(root, file)
                yield file_path


if __name__ == '__main__':
    print(get_base_proj_dir())
    PathOperation().make_dir_or_file('api_runner/log/debug/2.txt')

    print(PathOperation().ls_all_file_by_type('examples/suit_debug_yaml_1'))
