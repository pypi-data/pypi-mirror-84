'''
@File       :   setup.py
@Author     :   5478
@Version    :   1.2
'''
import setuptools
from setuptools import setup  # 这个包没有可以pip一下

with open("使用说明.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pystr",  # 这个是pip项目发布的名称
    version="1.2",  # 版本号，pip默认安装最新版
    keywords=("输入","汉字"),
    description="可以自动输入字符（包括汉字）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "许可证",

    packages=setuptools.find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["PyAutoGUI","pyperclip"]  # 该模块需要的第三方库
)