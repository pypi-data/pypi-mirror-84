# -*- coding: utf-8 -*-
'''
Created on 2020-11-6

@author: zhys513(254851907@qq.com)
'''   
import sys 
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from .settings import config 
from .core.response.BaseResponse import UnicornException
from .core.response.http_error import http_error_handler, unicorn_exception_handler
from .core.response.validation_error import http422_error_handler
from .core.events.events import create_stop_app_handler, create_start_app_handler 
from .core.logging.logging import LoggerFactory
from .core.router.router import router
 
# 初始化应用
application = FastAPI(title=config.PROJECT_NAME, version=config.VERSION, description=config.DESCRIPTION)
 
# 注入
def get_application() -> FastAPI:
    # Log
    application.state.log = LoggerFactory('log').logger
    # 添加事件
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))
     
    # 路由
    application.include_router(router)
    # 添加错误处理
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(UnicornException, unicorn_exception_handler)
 
    return application

def get_para(host = "0.0.0.0",port = 5000): 
    if len(sys.argv) != 1:
        for argv in sys.argv[1:]:
            if argv[:6] == "--port":
                port = int(argv.rsplit("=")[1])
            elif argv[:6] == "--host":
                host = argv.rsplit("=")[1]
    return host,port