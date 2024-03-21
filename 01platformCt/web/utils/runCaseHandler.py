# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     runCaseHandler.py
# Author:      Jakilo
# Datetime:    2024/3/4 09:52
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:  测试用例组装以及生成操作
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
from typing import Optional, List, Dict, Union, Type

from app import application
from common.lib.pathBase import PathOperation
from common.lib.shellBase import Shell
from common.lib.yamlBase import YamlHandler
from common.lib.jsonBase import JsonHandler
from common.lib.funcBase import BaseTools
from common.lib.timeBase import TimeBase
from common.modules.api_manage.apiInfoModel import ApiInfoModel
from common.modules.api_manage.apiCollectionModel import ApiCollectionModel
from common.modules.api_manage.apiCaseModel import ApiCaseModel
from common.modules.api_manage.apiHistoryModel import ApiHistoryModel
from web.utils.dbHandler import DbHandler

# 获取配置中指定的 临时文件生成地址
CASES_ROOT_DIR = application.config['API_CASES_ROOT_DIR']
DEBUG_CASES_ROOT_DIR = application.config['API_DEBUG_CASES_ROOT_DIR']
REPORT_ROOT_DIR = application.config['API_REPORT_ROOT_DIR']

execute_uuid: str = BaseTools.generate_uuid()
case_uuid: str = BaseTools.generate_uuid()
run_tmp_dir: str = ''

generate_current_strf_time = TimeBase.generate_current_strf_time


def generate_execute_uuid() -> str:
    global execute_uuid
    execute_uuid = BaseTools.generate_uuid()
    return execute_uuid


def loads_case_info_data(data_str) -> Optional[dict]:
    data_dict = {}
    for d in JsonHandler.loads_json(str(data_str).replace("'", '"')):
        data_dict.update({d["key"]: d["value"]})
    if len(data_dict.items()) > 0:
        return data_dict


def make_tmp_dir(collection_id: str = '') -> str:
    """
    根据 debug 执行的 uuid 以及配置的debug_case_root_file 生成当前这次执行的临时文件目录
    :param
    :return:
    """
    # 获得临时的执行目录
    global run_tmp_dir
    run_tmp_dir = PathOperation.path_join(DEBUG_CASES_ROOT_DIR, str(collection_id) + '-' + str(
        generate_current_strf_time()) + '-' + execute_uuid)
    # 创建临时文件目录
    PathOperation.make_dirs(run_tmp_dir)
    return run_tmp_dir


def write_test_case_context_data_by_yaml(context_data: dict, case_path_dir: str) -> bool:
    """
    将测试用例 context 数据写入到对应的 context.yaml中
    :param context_data:
    :param case_path_dir:
    :return:
    """
    if context_data:
        context_yaml_file = PathOperation.path_join(case_path_dir, "context.yaml")
        YamlHandler.write_yaml_file(context_yaml_file, context_data)
        return True
    return False


def make_case_context_file(debug_vars: dict) -> bool:
    """

    :param debug_vars:
    :param
    :return:
    """
    context_data = {}
    if debug_vars:
        print(debug_vars)
        for d in debug_vars:
            # for d in JsonHandler.loads_json(str(debug_vars).replace("'", '"')):
            print(d)
            context_data.update({d["key"]: d["value"]})
    if write_test_case_context_data_by_yaml(context_data, run_tmp_dir):
        return True
    return False


def make_testcase_by_api_info_in_yaml_format(api_info: ApiInfoModel) -> dict:
    """
    通过 apiInfo 模型的内容，生成对应的执行参数
    :param api_info:
    :return:
    """
    # 填充测试用例信息
    test_case_data = {
        "desc": api_info.api_name,
        "steps": [
            {
                "url": api_info.request_url,
                "method": api_info.request_method,
            }
        ]
    }
    # 0. 如果存在请求头，则添加请求头
    if api_info.request_headers:
        request_headers = loads_case_info_data(api_info.request_headers)
        if request_headers:
            test_case_data["steps"][0]["header"] = request_headers

    # 1. 仅在 data 不为空时添加
    if api_info.request_form_datas:
        request_form_datas = loads_case_info_data(api_info.request_form_datas)
        if request_form_datas:
            test_case_data["steps"][0]["data"] = request_form_datas

    # 2. 仅在 www_form_datas 不为空时添加
    if api_info.request_www_form_datas:
        requests_datas = loads_case_info_data(api_info.request_headers)
        if requests_datas:
            test_case_data["steps"][0]["data"] = requests_datas

    # 3.仅在 params 不为空时添加
    if api_info.request_params:
        requests_params = loads_case_info_data(api_info.request_headers)
        if requests_params:
            test_case_data["steps"][0]["params"] = requests_params

    # 4.仅在 json_data 不为空时添加
    if api_info.request_json_data:
        test_case_data["steps"][0]["json"] = api_info.request_json_data
    # 5.如果存在 前置脚本，则添加
    if api_info.pre_request:
        test_case_data["steps"][0]["pre_script"] = api_info.pre_request
    # 6.如果存在 后置脚本，则添加
    if api_info.post_request:
        test_case_data["steps"][0]["post_script"] = api_info.post_request
    return test_case_data


def write_case_file_by_yaml(case_data: dict, order: int = 1) -> str:
    case_file_name = BaseTools.generate_uuid()
    test_case_filename = f"{order}_{case_file_name}.yaml"
    test_case_yaml_file = PathOperation.path_join(run_tmp_dir, test_case_filename)
    YamlHandler.write_yaml_file(test_case_yaml_file, case_data)
    return test_case_yaml_file


def run_case_debug(_run_tmp_dir):
    # remote_command = f"ApiTestRun --case_path={run_tmp_dir} -sv --capture=tee-sys "
    remote_command = f"ApiTestRun --case_path={_run_tmp_dir}"
    return Shell.command_output(remote_command)


def del_debug_tmp_file(tmp_dir: str):
    PathOperation.rm_tree(tmp_dir)


def run_debug_case_info(api_info: ApiInfoModel) -> str:
    """
    获取文件路径，生成文件目录
    处理 debug 的 context
    处理数据为 yaml 文件
    写入文件
    调用运行器运行测试
    处理临时文件
    返回测试报告
    :param api_info:ApiInfoModel
    :param  TODO debug_type: str 根据 debug_type 来调用用例生成函数
    :return:
    """
    # 该次执行唯一ID
    _execute_uuid = generate_execute_uuid()
    # 1.测试初始化
    # 1.0 创建 该次执行对应的文件夹
    __run_tmp_dir = make_tmp_dir()
    application.logger.info(f'run_debug_case_info run_tmp_dir:{__run_tmp_dir}')
    print(f'run_debug_case_info run_tmp_dir:{__run_tmp_dir}')
    # 1.1 先组装 Debug变量 数据 生成 context.yaml 文件
    make_case_context_file(api_info.debug_vars)
    # 1.2 把数据转变为yaml 保存到 测试套件执行对应的文件夹
    test_case_data = make_testcase_by_api_info_in_yaml_format(api_info)
    application.logger.info(f'run_debug_case_info test_case_data:{test_case_data}')
    print(f'run_debug_case_info test_case_data:{test_case_data}')
    # 1.3 将测试用例数据写入 YAML 文件，格式为 执行顺序_名称.yaml
    write_case_file_by_yaml(test_case_data)
    application.logger.info(f'run_debug_case_info write_case_file run_tmp_dir:{__run_tmp_dir}')
    print(f'run_debug_case_info write_case_file run_tmp_dir:{__run_tmp_dir}')
    # 2.测试执行
    command_output = run_case_debug(__run_tmp_dir)
    application.logger.info(f'run_debug_case_info run_case_debug run_tmp_dir:{__run_tmp_dir}')
    print(f'run_debug_case_info run_case_debug run_tmp_dir:{__run_tmp_dir}')
    # 3.删除临时目录
    # del_debug_tmp_file(run_tmp_dir)
    history_desc = _execute_uuid + '\n' + command_output.split("\n")[-2].replace("=", "")
    return history_desc


def make_run_collection_report():
    # 需要导入 logHandler test_result_log_analysis，和 report 分析
    pass


def run_collection(collection_dir, report_data_path) -> str:
    # 封装测试命令  TODO 封装命令行支持 allure
    # remote_command = f"ApiTestRun --case_path={collection_dir} -sv --capture=tee-sys --alluredir={report_data_path} "
    _remote_command = f"ApiTestRun --case_path={collection_dir}   --pytest_args=--alluredir={report_data_path}"
    # 返回命令执行
    return Shell.command_output(_remote_command)


def make_allure_report(report_data_path, report_html_path) -> str:
    _remote_command = f"allure generate {report_data_path} -c -o {report_html_path}"
    return Shell.command_output(_remote_command)


def run_case_collection(collection: Union[ApiCollectionModel], case_model: Union[Type[ApiCaseModel]],
                        info_model: Union[Type[ApiInfoModel]], history_model: Union[Type[ApiHistoryModel]]) -> (
int, str):
    """
    1. 判断是否有 collection_params 如果有 collection_params 代表 可能需要 多次执行该套件
    2. 循环 collection_params
        2.1. 生成测试套件以及文件夹  执行唯一的 uuid
        2.2. 组装环境变量
        2.3. 生成测试用例数据保存到套件对应的执行文件夹  ApiCase
            2.3.1 遍历 apicase，渲染信息并写入
                # 2.3.1.1 获得对应的 caseInfo信息
                # 2.3.3.2 获得case_info对应的 test_case_data
                # 2.3.3.3 更新 apiCase 的 ddts 参数
                # 2.3.3.4 将测试用例数据写入 YAML 文件，格式为 执行顺序_名称.yaml
        2.4. 文件生成，相关依赖文件夹（报告）
        2.5. 测试引擎执行  TODO 逻辑是否需要一次 run 所有的 collections
        2.6. 生成测试报告 ApiHistoryModel
        2.7. 删除临时文件
    :return:
    """
    # 1. 检查 collection_params 参数
    application.logger.info(f'run_case_collection 1. 检查 collection_params 参数 开始')

    collection_params: List[Dict] = [{}]  # 初始化一个空
    # 如果有 collection_params 代表 可能需要 多次执行该套件
    if collection.collection_params:
        collection_params: List[Dict] = JsonHandler.loads_json(collection.collection_params)
    application.logger.info(f'run_case_collection 1. 检查 collection_params 参数 完成')
    print(f'collection_params{collection_params}')
    # 2. 循环 collection_params
    for collection_param in collection_params:
        # 2.1. 生成测试套件以及文件夹  执行唯一的 uuid
        _execute_uuid = generate_execute_uuid()
        _run_tmp_dir = make_tmp_dir(collection.id)
        application.logger.info(f'run_case_collection 2.1. 生成测试套件以及文件夹  执行唯一的 uuid 完成')
        print(f'run_case_collection 2.1. 生成测试套件以及文件夹  执行唯一的 uuid 完成')
        # 2.2. 组装环境变量
        print(f'collection_param{collection_param}')
        case_context = {}
        if collection_param:
            case_context.update(collection_param)
        if collection.collection_env:
            print(f'collection.collection_env{collection.collection_env}')
            case_context.update(collection_param)
        if case_context:
            write_test_case_context_data_by_yaml(case_context, _run_tmp_dir)
        application.logger.info(f'run_case_collection 2.2. 组装环境变量 完成')
        print(f'run_case_collection 2.2. 组装环境变量 完成')
        # 2.3. 生成测试用例数据保存到套件对应的执行文件夹  ApiCase
        application.logger.info(f'run_case_collection 2.3. 生成测试用例数据保存到套件对应的执行文件夹  ApiCase开始')
        print(f'run_case_collection 2.3. 生成测试用例数据保存到套件对应的执行文件夹  ApiCase 开始')
        cases: List[ApiCaseModel] = DbHandler.query_by_filter_by_all(case_model, collection_id=collection.id)
        # 2.3.1 遍历 apicase，渲染信息并写入Yaml
        for case in cases:
            # 2.3.1.1 获得对应的 caseInfo信息
            # TODO 这里要支持，不同 case_info的选择逻辑
            application.logger.info(f'run_case_collection 2.3.1.1 获得对应的 caseInfo信息 开始')
            print(f'run_case_collection 2.3.1.1 获得对应的 caseInfo信息 开始')
            case_info: [Union[ApiInfoModel]] = DbHandler.query_by_filter_by_first(info_model, id=case.api_info_id)

            # 2.3.3.2 获得case_info对应的 test_case_data
            application.logger.info(f'run_case_collection  2.3.3.2 获得case_info对应的 test_case_data 开始')
            print(f'run_case_collection  2.3.3.2 获得case_info对应的 test_case_data 开始')
            # TODO写入的方式仅支持 apiInfo 直接写入，apiCase 的情况需要进行判断
            test_case_data = make_testcase_by_api_info_in_yaml_format(case_info)
            application.logger.info(f'run_case_collection  2.3.3.2 获得case_info对应的 test_case_data 完成{test_case_data}')
            # 2.3.3.3 更新 apiCase 的 ddts 参数
            application.logger.info(f'run_case_collection 2.3.3.3 更新 apiCase 的 ddts 参数 开始')
            print(f'run_case_collection 2.3.3.3 更新 apiCase 的 ddts 参数 开始')
            params_data = case.param_data or None
            if params_data:
                print(f'in params_data:{params_data}')
                test_case_data.update({'ddts': JsonHandler.loads_json(params_data)})
                # test_case_data["ddts"] = loads_data(params_data)
            # 2.3.3.4 将测试用例数据写入 YAML 文件，格式为 执行顺序_名称.yaml
            application.logger.info(f'run_case_collection 2.3.3.4 将测试用例数据写入 YAML 文件，格式为 执行顺序_名称.yaml 开始')
            print(f'run_case_collection 2.3.3.4 将测试用例数据写入 YAML 文件，格式为 执行顺序_名称.yaml 开始')
            write_case_file_by_yaml(test_case_data, order=case.run_order)
        # 2.4. 文件生成，相关依赖文件夹（报告）
        application.logger.info(f'run_case_collection2.4. 文件生成，相关依赖文件夹（报告） 开始')
        print(f'run_case_collection 2.4. 文件生成，相关依赖文件夹（报告） 开始')
        report_data_path = PathOperation.path_join(REPORT_ROOT_DIR, f"{_execute_uuid}-data")  # 测试数据
        report_html_path = PathOperation.path_join(REPORT_ROOT_DIR, _execute_uuid)  # 测试html报告
        # 2.5. 测试引擎执行  TODO 逻辑是否需要一次 run 所有的 collections
        application.logger.info(f'run_case_collection 2.5. 测试引擎执行 开始')
        print(f'run_case_collection 2.5. 测试引擎执行 开始')
        command_output = run_collection(_run_tmp_dir, report_data_path)
        if 'Error' in command_output:
            return 0, command_output
            # 2.6. 生成测试报告 ApiHistoryModel
        application.logger.info(f'run_case_collection 2.6. 生成测试报告 ApiHistoryModel 开始')
        print(f'run_case_collection 2.6. 生成测试报告 ApiHistoryModel 开始')
        history_desc = _execute_uuid + '\n' + command_output.split("\n")[-2].replace("=", "")
        # TODO 这里可以根据 command_output 命令输出的内容去做一些统计
        cmd_output = make_allure_report(report_data_path, report_html_path)
        application.logger.info(f'run_case_collection 2.6. 生成测试报告命令行结果 {cmd_output}')
        application.logger.info(f'run_case_collection 2.6. 生成测试报告完成 {report_html_path}')
        # 2.7. 删除临时文件
        application.logger.info(f'run_case_collection 2.7. 删除临时文件开始')
        print(f'run_case_collection 2.3.1.1 获得对应的 caseInfo信息 开始')
        # Shell.rmtree(_run_tmp_dir)
        # Shell.rmtree(report_data_path)
        # 2.8 返回测试结果
        application.logger.info(f'run_case_collection 2.8 返回测试结果 开始')
        print(f'run_case_collection 2.8 返回测试结果 开始')
        # TODO 扩展其他报告支持
        history_context = {
            'id': 0,
            'collection_id': collection.id,
            'history_desc': history_desc,
            'history_detail': _execute_uuid + cmd_output
        }
        his_report_id = DbHandler.create_action(history_model, history_context)
        application.logger.info(f'run_case_collection  完成')
        print(f'run_case_collection  完成')
        return his_report_id, f'执行完成测试结果地址{report_data_path},测试报告地址{report_html_path}'


if __name__ == '__main__':
    execute_uuid = generate_execute_uuid()
    run_tmp_dir = make_tmp_dir()
    write_case_file_by_yaml({'desc': '测试百度', 'steps': [{'url': 'www.baidu.com', 'method': 'GET'}]})
