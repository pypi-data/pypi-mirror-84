#! /usr/bin/env python
from setuptools import setup, find_packages
setup(
 name = 'assasin64',
 version = '0.0.1',
 description = 'library ',
 long_description = 'library ',
 author = 'assasin',
 author_email = 'assasin0308@sina.com',
 license = 'MIT Licence',
 keywords = 'testing just for fun ',
 platforms = 'any',
 python_requires = '>=3.7.*',
 install_requires = [],
 package_dir = {'': 'src'},
 packages = find_packages('src')
 )