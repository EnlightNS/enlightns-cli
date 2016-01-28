EnlightNS.com Command Line Interface

.. image:: https://travis-ci.org/EnlightNS/enlightns-cli.svg?branch=master
    :target: https://travis-ci.org/EnlightNS/enlightns-cli

.. image:: https://img.shields.io/pypi/v/enlightns-cli.svg
    :target: https://pypi.python.org/pypi/enlightns-cli

.. image:: https://img.shields.io/pypi/dm/enlightns-cli.svg
        :target: https://pypi.python.org/pypi/enlightns-cli


.. contents:: Table of Contents


Installation
============

Ubuntu 14.04 or higher
----------------------

If the python package installer is not installed

::

    sudo apt-get install python-pip python-dev

You need the following libraries

::

    sudo apt-get install libffi-dev libssl-dev

Install the command line interface

::

    sudo pip install enlightns-cli

or

::

    sudo easy_install enlightns-cli

Mac OS (Yosemite)
-----------------

If you don't have python installed

::

    brew install python

You might need these libraries

::

    brew install pkg-config libffi

Install the command line interface

::

    sudo pip install enlightns-cli

Centos 6
--------

If python is not installed

::

    sudo yum install python-devel python-setuptools

If GCC the C compiler is not installed, you might get the following
error

::

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

::

    sudo yum install gcc

You need the following libraries

::

    sudo yum install libffi-devel openssl-devel

If python was not installed

::

    sudo easy_install pip

Install the command line interface

::

    sudo pip install enlightns-cli

or

::

    sudo easy_install enlightns-cli


Packages
--------

We also provide compiled packages hosted on

.. image:: https://www.bintray.com/docs/images/bintray_badge_color.png
        :target: https://bintray.com/enlightns/debian/enlightns-cli/view?source=watch

Ubuntu or Debian
^^^^^^^^^^^^^^^^

::

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 379CE192D401AB61
    echo "deb http://dl.bintray.com/enlightns/debian /" | sudo tee -a /etc/apt/sources.list

CentOS or Fedora
^^^^^^^^^^^^^^^^

::

    # Centos or Fedora
    .. coming soon ..

Bash completion
---------------

To setup the bash completion execute the following command line

::

    enlightns-cli bash >> ~/.bashrc
    source ~/.bashrc

Development
===========

Testing or building the app
---------------------------

Clone the repository and activate a virtualenv or not a virtualenv Once
it is activated move in the repository folder and execute the following
command line:

::

    cd enlightns-cli
    pip install --editable .

**Important notice you can test your changes without uninstalling and
reinstalling.**

Execute the unit tests
----------------------

::

    make test

Removing the CLI
----------------

If you wish to uninstall the command line

::

    pip uninstall -y enlightns-cli
    
Usage
=====

How to use the command line tool to configure your hostname to be updated periodically.

::

    # Login
    enlightns-cli authenticate
    
    # Bash completion if you want it
    enlightns-cli bash >> ~/.bashrc

    # configure your record that you previously created on the dashboard at https://enlightns.com/
    enlightns-cli setup --help
    enlightns-cli setup -r home-lakhdar.enlightns.info -w wan
    
    # update the client with your ip
    enlightns-cli update -f
    
    # install the scheduled job for your system to update
    enlightns-cli cron -a

