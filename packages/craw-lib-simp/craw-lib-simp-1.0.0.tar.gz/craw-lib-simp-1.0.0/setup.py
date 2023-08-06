# coding:utf8
from setuptools import setup, find_packages

setup(
    name='craw-lib-simp',  # 应用名
    version='1.0.0',  # 版本号
    packages=find_packages(),  # 包括在安装包内的 Python 包
    description='crawler lib',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
    package_data={
        '': ['*.py']
    },
    keywords=['crawler', 'lib'],
)
