# -*- coding: utf-8 -*-
'''
Created on 2020-11-6

@author: zhys513(254851907@qq.com)
'''
#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='opspipe.app',
    version='0.0.1',
    description='A simple uniform interface',
    long_description='opspipe: https://gitee.com/zhys513/theta_task',
    license='Apache License 2.0',
    url='https://gitee.com/zhys513/theta_task',
    author='zhys513',
    author_email='254851907@qq.com',
    install_requires=['fasetapi>=0.61.1'],
    packages=find_packages()
)