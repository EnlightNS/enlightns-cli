# -*- coding: utf-8 -*-
from setuptools import find_packages
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import re


version = ''
with open('enscli/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

def get_requirements():
    """Simply read the requirements.txt file and returns the list of the dependencies.

    :returns: list of requirements
    """
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

    return requirements

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='enlightns-cli',
    version=version,
    description='EnlightNS.com Command Line Interface.',
    long_description='See the long description on https://github.com/EnlightNS/enlightns-cli',
    author='Dominick Rivard',
    author_email='support@enlightns.com',
    maintainer="Dominick Rivard",
    maintainer_email = "support@enlightns.com",
    url='http://enlightns.com/',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'enlightns-cli=enscli.scripts.cli:cli',
        ],
    },
    package_data={
        '': ['LICENSE', '*.sh'],
        'enscli.scripts': ['bash_complete.sh'],
    },
)
