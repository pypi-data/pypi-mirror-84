#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os, json
#os.environ["CUDA_VISIBLE_DEVICES"] = "1"  
import uvicorn  
from opspipe.app.settings.config import DEBUG
from opspipe.app.main import get_application,get_para
from opspipe.app.core.response.BaseResponse import success, fail 
from fastapi import Query  
from pydantic import BaseModel
from project_design_approval import get_result
# -------------------- System --------------------   
app = get_application()
app.description =  '工程项目初步设计批复抽取'
 
 
 
class Item(BaseModel):
    text: str = Query(
        '',
        description="待抽取文本",
        deprecated=True
    )


@app.post("/predict",summary="纯文本抽取接口")
async def predict(item: Item):
    text = item.dict()['text']
    result = get_result(text)
    return success(result)
  
     
if __name__ == '__main__':
    host , port = get_para()
    uvicorn.run(app='__main__:app', host=host, port=port, reload=True, debug=DEBUG)
