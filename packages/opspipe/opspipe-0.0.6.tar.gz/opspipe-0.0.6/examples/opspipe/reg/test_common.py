# -*- coding: utf-8 -*-
'''
Created on 2020-11-9

@author: zhys513(254851907@qq.com)
'''

from opspipe.reg.common import regularExtrator


if __name__ == "__main__":
    text = '急寻特朗普，男孩，于2018年11月27号11时在陕西省安康市汉滨区走失。丢失发型短发，...如有线索，请迅速与警方联系：18100065143，132-6156-2938，baizhantang@sina.com.cn 和yangyangfuture at gmail dot com'
    ex = regularExtrator(text)
    print("chinese cellphone:")
    print(ex.extract_chinese_cellphone())
    print("email:")
    print(ex.extract_email())
    print("id:")
    print(ex.extract_indentity_ids())
    print("date:")
    print(ex.extract_date())
    print("datetime:")
    print(ex.extract_datetime())