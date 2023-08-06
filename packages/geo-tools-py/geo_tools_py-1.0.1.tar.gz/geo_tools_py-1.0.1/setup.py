# Copyright 2020 donggee.

"""
The setup script to install Geo SDK for python
"""
from __future__ import absolute_import
import io
import os
import re
try:
    from setuptools import setup,Extension
except ImportError:
    from distutils.core import setup

# with io.open(os.path.join("geo", "__init__.py"), "rt") as f:
#     SDK_VERSION = re.search(r"SDK_VERSION = b'(.*?)'", f.read()).group(1)
with open(os.path.join("./", "README.md"), "rt",encoding='utf-8') as f:
    LONG_DESC=f.read()

setup(
    name='geo_tools_py',
    version='v1.0.1',
    install_requires=['requests'],
    python_requires='>=2.7',
    packages=['GeoData','GeoCal','example'],
    url='http://datahub.wtf',
    license='Apache License 2.0',
    author='caidong',
    author_email='zhucaidong@aliyun.com',
    description='Geo SDK for python',
    long_description=LONG_DESC,
    long_description_content_type='text/markdown',
)
