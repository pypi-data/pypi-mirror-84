# -*- coding: utf-8 -*-
'''
Created on 2020-11-9

@author: zhys513(254851907@qq.com)
'''

from opspipe.reg.scanner import regularExtrator
from opspipe.reg.common import regularExtrator as cRegularExtrator
from opspipe.base.logger import logtime 
'''
提取字段：批复发文单位、发文号、发文名称、发文日期、项目列表（项目地点、项目名称、对应网格编号、对应可研项目名称、概算总费用（收口）（含金额单位）、概算总费用（不含税）（含金额单位）、设计费（含金额单位）、安装费（含金额单位）、监理费（含金额单位））
'''

# 批复发文单位
def get_qualification_certificate(txt): 
    ex = regularExtrator(txt)  
    ex.split_txt('― 2 ―') 
    ex.text = ex.data_list[0]
    #ex.print_list()
    ex.split_txt(r'― 1 ―')
    ex.text = ex.data_list[1]
    #ex.print_txt()
    ex.split_txt(r'\d年\d月\d日')
    ex.print_txt()
    ex.text = ex.data_list[0]
    #ex.scan_for_mlists(['公司','有限','国网'])
    #ex.print_list()
    #ex.text = ex.data_list[0]
    #ex.clear_txt(r'\n')
    #ex.match_txt_o(pattern)
    #ex.print_txt()
    return ex.text


# 发文号
def get_enterprise_name(txt):
    ex = regularExtrator(txt) 
    ex.split_txt('企业名称:')
    #ex.print_list()
    ex.text = ex.data_list[1]
    ex.split_txt('\n')  
    ex.text = ex.data_list[0]
    #ex.print_txt()
    return ex.text


# 发文名称
def get_addr_detailed(txt):
    ex = regularExtrator(txt) 
    ex.split_txt('详细地址:')
    #ex.print_list()
    ex.text = ex.data_list[1]
    ex.split_txt('\n')  
    ex.text = ex.data_list[0]
    #ex.print_txt()
    return ex.text

 
# 发文日期
def get_unified_social_credit_code(txt):
    ex = regularExtrator(txt) 
    ex.split_txt('法定代表人:')
    ex.text = ex.data_list[0]
    ex.split_txt('\n')  
    #ex.print_list() 
    ex.text = ex.scan_for_lists_p('\d{6}')[0]
    cre = cRegularExtrator(ex.text)
    ex.text = cre.remove_chinese()
    ex.clear_txt() 
    return ex.text


# 项目列表（项目地点、项目名称、对应网格编号、对应可研项目名称、概算总费用（收口）（含金额单位） 
def get_legal_representative(txt):
    ex = regularExtrator(txt) 
    ex.split_txt('法定代表人:')
    #ex.print_list()
    ex.text = ex.data_list[1]
    ex.split_txt('\n')  
    ex.text = ex.data_list[0]
    ex.clear_txt()
    #ex.print_txt() 
    return ex.text


# 概算总费用（不含税）（含金额单位）
def get_registered_capital(txt):
    ex = regularExtrator(txt) 
    ex.split_txt('注册资本:')
    #ex.print_list()
    ex.text = ex.data_list[1]
    ex.split_txt('\n')  
    ex.text = ex.data_list[0]
    ex.clear_txt()
    #ex.print_txt() 
    return ex.text
 
# 设计费（含金额单位）
def get_economic_nature(txt):
    ex = regularExtrator(txt) 
    ex.split_txt('经济性质:')
    #ex.print_list()
    ex.text = ex.data_list[1]
    ex.split_txt(r'证书编号:')  
    ex.text = ex.data_list[0]
    ex.clear_txt()
    return ex.text

# 安装费（含金额单位）
def get_certificate_number(txt):
    ex = regularExtrator(txt) 
    ex.split_txt('证书编号:')
    #ex.print_list()
    ex.text = ex.data_list[1]
    ex.split_txt(r'有效期:')  
    ex.text = ex.data_list[0]
    ex.clear_txt()
    return ex.text

# 监理费（含金额单位））
def get_validity_date(txt):
    ex = regularExtrator(txt) 
    ex.split_txt('有效期:')
    #ex.print_list()
    ex.text = ex.data_list[1]
    ex.split_txt(r'发证机关:')  
    ex.text = ex.data_list[0]
    ex.text = ex.split_txt('\n')[0]
    ex.clear_txt()
    return ex.text
 

@logtime
def get_result(txt):
    
    # 资质证书名称
    qualification_certificate = get_qualification_certificate(txt)

    # 企业名称
    #enterprise_name = get_enterprise_name(txt)

    # 详细地址
    #addr_detailed = get_addr_detailed(txt)
 
    # 统一社会信用代码
    #unified_social_credit_code = get_unified_social_credit_code(txt)

    # 法定代表人
    #legal_representative = get_legal_representative(txt)

    # 注册资本
    #registered_capital = get_registered_capital(txt)
 
    # 经济性质
    #economic_nature = get_economic_nature(txt)

    #证书编号
    #certificate_number = get_certificate_number(txt)

    #有效期
    #validity_date = get_validity_date(txt)
    
    result = {"qualification_certificate": qualification_certificate,
              #"enterprise_name": enterprise_name,
              #"addr_detailed": addr_detailed,
              #"unified_social_credit_code": unified_social_credit_code,
              #"legal_representative": legal_representative,
              #"registered_capital": registered_capital,
              #"economic_nature": economic_nature,
              #"certificate_number": certificate_number, 
              #"validity_date": validity_date,
              }
 
    return result