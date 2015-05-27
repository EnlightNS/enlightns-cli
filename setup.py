# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from setuptools import setup, find_packages
import re

version = ''
with open('enscli/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

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
    py_modules=['enscli', ],  # List the modules within the enlightns-cli project.
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2.0',
    zip_safe=False,classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ),
    install_requires=[
        'click==4.0',
        'colorama==0.3.3',
        'netifaces==0.10.4',
        'python-crontab==1.9.3',
        'python-dateutil==2.4.2',
        'requests==2.7.0',
        'six==1.9.0',
    ],
    entry_points='''
        [console_scripts]
        enlightns-cli=enscli.scripts.cli:cli
    ''',
)
