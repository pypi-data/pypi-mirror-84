'''
@File       :   setup.py
@Author     :   Liu Wei
@Time       :   2020-11-05 17:34
@Version    :   1.0
@Contact    :   275901905@qq.com
@Dect       :   None
'''
 
from setuptools import setup, find_packages     # 这个包没有可以pip一下
 
setup(
    name = "mutiplexing",      # 这个是pip项目发布的名称
    version = "1.0.0",      # 版本号，pip默认安装最新版
    keywords = ("pip", "mutiplexing","mp"),
    description = "数据分析复用模块",
    long_description = "数据分析复用模块",
    license = "MIT Licence",
 
    # url = "https://github.com/jiangfubang/balabala",       # 项目相关文件地址，一般是github，有没有都行吧
    author = "Liu Wei",
    author_email = "luckybang@163.com",
 
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy","pandas","time"]        # 该模块需要的第三方库
)