# -*- coding: utf-8 -*-
'''
各种数据读取工具
Created on 2020-9-29
@author: zhys513(254851907@qq.com)
'''
import json, os,re
import os, zipfile
import shutil

def clean_text(text):
    text = str(text)
    if text:
        text = text.strip()
        #  text = re.sub('\t', ' ', text)
    return text

def make_zip(source_dir, output_filename):
    '''打包目录为zip文件（未压缩）'''
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
 
 
def un_zip(file_name):  
    """unzip zip file"""  
    zip_file = zipfile.ZipFile(file_name)  
    if os.path.isdir(file_name + "_files"):  
        pass  
    else:  
        os.mkdir(file_name + "_files")  
    for names in zip_file.namelist():  
        zip_file.extract(names,file_name + "_files/")  
    zip_file.close()  


def read_txts(filename):
    '''读取单个txt文件，文件中包含多行，返回[]'''
    with open(filename, encoding='utf-8') as f:
        return f.readlines()


def read_txt(filename):
    '''读取单个txt文件的数据'''
    with open(filename, encoding='utf-8') as f:
        return f.read()


def read_json(filename):
    '''读取单个json类型文件，并load为dict'''
    with open(filename, mode='r', encoding='utf8') as f:
        return json.load(f)


def load_jsons(file_path):
    '''读取多个json类型文件，并装在到[] TODO'''
    D = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        for l in f:
            l = json.loads(l)
            D.append(l)
    return D


def validateEmail(email):
    email_reg = r'^[a-zA-Z0-9_.-]+[#@][a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[.a-zA-Z0-9]{2,6}'
    #email_reg = r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}'
    ret_1 = re.findall(email_reg, email)
    if ret_1:
        return True
    return False

def copy_dir(src_path, target_path):
    '''拷贝文件夹到指定目录'''
    if os.path.isdir(src_path) and os.path.isdir(target_path):
        filelist_src = os.listdir(src_path)
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copy_dir(path, path1)
            else:
                with open(path, 'rb') as read_stream:
                    contents = read_stream.read()
                    path1 = os.path.join(target_path, file)
                    with open(path1, 'wb') as write_stream:
                        write_stream.write(contents)
        return True

    else:
        return False



def copy_dirs(src_path,target_path):
    '''拷贝指定文件夹中的文件到指定目录，没有目录结构'''
    file_count=0
    source_path = os.path.abspath(src_path)
    target_path = os.path.abspath(target_path)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target_path)
                file_count+=1
                print(src_file)
    return int(file_count)