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


## Centos 6.



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
    
Execute the unit tests

    
    

**Important notice you can test your changes without uninstalling and reinstalling.**

# Removing the CLI

    pip uninstall -y enlightns-cli