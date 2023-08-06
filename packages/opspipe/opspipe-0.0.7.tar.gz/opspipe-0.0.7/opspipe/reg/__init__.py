# -*- coding: utf-8 -*-
class regularExtrator():

    def __init__(self, text='',data_list = []):
        self.text = text
        self.data_list = data_list
    
    def select_list(self,start_index = 0, end_index = 0): 
        # list 范围选取
        list_len = len(self.data_list)
        if end_index == 0:
            end_index = list_len 
        self.data_list = self.data_list[start_index:end_index]   
        return self.data_list
    
    def select_txt(self,start_index = 0, end_index = 0): 
        # 文本 范围选取
        txt_len = len(self.text)
        if end_index == 0:
            end_index = txt_len 
        self.text = self.text[start_index:end_index]   
        return self.text
    
    def print_txt(self,uid='-'):
        print(f'text({uid})>>>',self.text)
         
    def print_list(self,uid='-'):
        print(f'list({uid})>>>',self.data_list)