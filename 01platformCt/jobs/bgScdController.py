# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   01platformCt
# FileName:     clean_expired_tokens_job.py
# Author:      Jakilo
# Datetime:    2024/2/23 10:59
# email：       1192788767@qq.com
# github:       Jakilo1996
# Description:
# 命名规则  目录名小写字母+下划线，文件名 小驼峰，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

from apscheduler.schedulers.background import BackgroundScheduler
# 定时清理 token
print(f'after clean_expired_tokens_crontab')
from web.utils.jwtUtil import clean_expired_tokens_crontab


def background_scheduler_run():
    # 创建后台调度器
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_expired_tokens_crontab, 'interval', minutes=30)  # 每隔 10 分钟执行一次清理过期 Token 的任务
    scheduler.start()  # 启动调度器

