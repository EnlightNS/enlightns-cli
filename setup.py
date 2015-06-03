# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from setuptools import setup, find_packages
import re


version = ''
with open('enscli/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

if not version:
    raise RuntimeError('Cannot find version information')

packages = [
    'enscli',
    'enscli.scripts',
    'enscli.rest',
]

setup(
    name='enlightns-cli',
    version=version,
    description='EnlightNS.com Command Line Interface.',
    long_description='See the long description on http://enlightns.com/about/',
    author='Dominick Rivard',
    author_email='support@enlightns.com',
    url='http://enlightns.com/',
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ),
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        enlightns-cli=enscli.scripts.cli:cli
    ''',
)
