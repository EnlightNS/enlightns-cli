EnlightNS.com Command Line Interface

[![Build Status](https://travis-ci.org/EnlightNS/enlightns-cli.svg?branch=develop)](https://travis-ci.org/EnlightNS/enlightns-cli)

# Installation

## Ubuntu 14.04 or higher

If the python package installer is not installed 
    
    sudo apt-get install python-pip

You need the following libraries

    sudo apt-get install libffi-dev libssl-dev
    
Install the command line interface

    sudo pip install enlightns-cli
    
or 
    
    sudo easy_install enlightns-cli
   
    
## Mac OS (Yosemite)

If you don't have python installed

    brew install python
    
Install the command line interface

    sudo pip install enlightns-cli


## Centos 6

You need the following libraries

    sudo yum install libffi-devel openssl-devel
    
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
    
