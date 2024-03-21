# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     www.py
# Author:      Jakiro
# Datetime:    2024/1/9 20:47
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

from app import application

# 蓝图过滤机制，指定route命令，去处理不同的请求
try:
    from web.ct.debugController import route_debug
    from web.ct.sys_manage import indexController, userController
    from web.ct.api_manage import apiCaseController, apiProjectController, apiModuleController, apiCollectionController, \
        apiHistoryController, apiInfoController

    application.register_blueprint(route_debug)
    application.register_blueprint(indexController.module_route)
    application.register_blueprint(userController.module_route)
    application.register_blueprint(apiProjectController.module_route)
    application.register_blueprint(apiModuleController.module_route)
    application.register_blueprint(apiHistoryController.module_route)
    application.register_blueprint(apiCollectionController.module_route)
    application.register_blueprint(apiInfoController.module_route)
    application.register_blueprint(apiCaseController.module_route)


except Exception as e:
    import traceback

    traceback.print_exc()
