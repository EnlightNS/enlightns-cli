EnlightNS.com Command Line Interface

[![Build Status](https://travis-ci.org/EnlightNS/enlightns-cli.svg?branch=develop)](https://travis-ci.org/EnlightNS/enlightns-cli)
[![Latest Version](https://pypip.in/version/enlightns-cli/badge.svg)](https://pypi.python.org/pypi/enlightns-cli/)

# Installation

## Ubuntu 14.04 or higher

If the python package installer is not installed 
    
    sudo apt-get install python-pip python-dev

You need the following libraries

    sudo apt-get install libffi-dev libssl-dev
    
Install the command line interface

    sudo pip install enlightns-cli
    
or 
    
    sudo easy_install enlightns-cli
   
    
## Mac OS (Yosemite)

If you don't have python installed

    brew install python
    
You might need these libraries

    brew install pkg-config libffi
    
Install the command line interface

    sudo pip install enlightns-cli


## Centos 6

If python is not installed

    sudo yum install python-devel python-setuptools
    
If GCC the C compiler is not installed, you might get the following error

    Collecting cffi==1.2.1 (from enlightns-cli)
    Downloading cffi-1.2.1.tar.gz (335kB)
    100% |################################| 335kB 3.5MB/s 
    Complete output from command python setup.py egg_info:
    unable to execute gcc: No such file or directory
    unable to execute gcc: No such file or directory
    
        No working compiler found, or bogus compiler options
        passed to the compiler from Python's distutils module.
        See the error messages above.
        (If they are about -mno-fused-madd and you are on OS/X 10.8,
        see http://stackoverflow.com/questions/22313407/ .)
    compiling '_configtest.c':
    __thread int some_threadlocal_variable_42;
    compiling '_configtest.c':
    int some_regular_variable_42;
    
If you need to install GCC

    sudo yum install gcc

You need the following libraries

    sudo yum install libffi-devel openssl-devel
    
If python was not installed

    sudo easy_install pip
    
Install the command line interface

    sudo pip install enlightns-cli
    
or 

    sudo easy_install enlightns-cli


## Bash completion

To setup the bash completion execute the following command line

    enlightns-cli bash >> ~/.bashrc
    source ~/.bashrc


# Testing or building the app

Clone the repository and activate a virtualenv or not a virtualenv
Once it is activated move in the repository folder and execute the following
command line:

    cd enlightns-cli
    pip install --editable .
    
**Important notice you can test your changes without uninstalling and reinstalling.**
    
# Execute the unit tests

    make test

# Removing the CLI
If you wish to uninstall the command line

    pip uninstall -y enlightns-cli
    
