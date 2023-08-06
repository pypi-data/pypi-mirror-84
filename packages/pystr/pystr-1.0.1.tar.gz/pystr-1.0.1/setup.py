'''
@File       :   setup.py
@Author     :   5478
@Version    :   1.0.1
'''
import setuptools
from setuptools import setup, find_packages  # 这个包没有可以pip一下

setup(
    name="pystr",  # 这个是pip项目发布的名称
    version="1.0.1",  # 版本号，pip默认安装最新版
    keywords=("pip", "words", "write"),
    description="可以自动输入字符（包括汉字）",
    license = "许可证",

    packages=setuptools.find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["PyAutoGUI","pyperclip"]  # 该模块需要的第三方库
)