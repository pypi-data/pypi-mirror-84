# -*- coding: utf-8 -*-
import re
from ..reg import regularExtrator as pre

class regularExtrator(pre):

    def __init__(self, text='',data_list = []):
        pre.__init__(self, text, data_list)  
        self.text = text
        self.data_list = data_list
        
    def clear_list(self,pattern = r'[\s]*'):
        # 去除空格换行符等字符的txt文本列表
        data_drop = []
        for item in self.data_list: 
            txt_drop = re.sub(pattern, '', item)       # 清除换行,制表,空格
            data_drop.append(txt_drop)
        self.data_list = data_drop
        return data_drop 
    
    def clear_txt(self,pattern = r'[\s]*'):
        # 去除空格换行符等字符的txt文本列表  
        txt_drop = re.sub(pattern, '', self.text)       # 清除换行,制表,空格 
        self.text = txt_drop
        return txt_drop 
