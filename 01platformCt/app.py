from flask import Flask
# flask orm 管理
from flask_sqlalchemy import SQLAlchemy
# flask manage 管理
from flask_script import Manager
# flask 跨域
from flask_cors import CORS
# flask token 解决方案
from flask_jwt_extended import JWTManager

# flask 数据库迁移
from flask_migrate import Migrate
# Flask-WTF 的 CSRF 保护机制
from flask_wtf.csrf import CSRFProtect

import sys
import os

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 添加项目根目录报的导入
sys.path.append(current_dir)
print(f'app:{current_dir}')
# 导入配置信息
from config.devSettings import Config

from jobs.bgScdController import background_scheduler_run
import www


class Application(Flask):
    def __init__(self, import_name):
        """
        通过 Flask 父类的初始化方法，通过配置类配置初始化信息，并将 db 操作与 app 绑定，绑定 jwt
        :param import_name:
        """
        super(Application, self).__init__(import_name)  # 调用父类方法启动
        self.config.from_object(Config)
        db.init_app(self)
        jwt.init_app(self)


db = SQLAlchemy()
# 实例化 jwt 生成请求 token
jwt = JWTManager()
application = Application(__name__)
# 设置允许请求跨域
# CORS(application, resource=r'/*')

CORS(application, resources=application.config.get('CORS_RESOURCES'), origins=application.config.get('CORS_ORIGINS'))
# Flask-WTF 的 CSRF 保护机制
csrf = CSRFProtect(application)
# 将 app 交给 manager 托管
manage = Manager(application)

# CORS(application, resources=r'/*', supports_credentials=True, origin='http://localhost:5173')

# 设置数据库迁移
# migrate = Migrate(application, db)
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == '__main__':
    application.run()
    background_scheduler_run()
