import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django_softdeletion',  # 包名称
    version='0.1.0',  # 版本
    license='MIT',
    description='django softdeletion',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    zip_safe=False,
    packages=['django_softdeletion'],  # 包含的包列表
    include_package_data=True,
    install_requires=[
        'django'
    ],
)
