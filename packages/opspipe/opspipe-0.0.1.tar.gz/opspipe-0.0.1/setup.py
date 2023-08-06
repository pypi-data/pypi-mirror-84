from setuptools import setup, find_packages  
setup(
    name='opspipe',
    version='0.0.1',
    description="This is the ml pipeline",
    author='zhys513',#作者
    author_email="254851907@qq.com",
    url="https://gitee.com/zhys513/opspipe",
    #packages=find_packages(),
    packages=["opspipe", 
              "opspipe/app", 
              "opspipe/base", 
              "opspipe/utils", 
              #"opspipe/DevOps", 
              #"opspipe/DevOps/http", 
              #"opspipe/ner", 
              #"opspipe/ner/theta",
              #"opspipe/ner/utils"
              ],  #这里是所有代码所在的文件夹名称
    install_requires=['requests'],
    python_requires='>=3.6',
)

