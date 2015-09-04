EnlightNS.com Command Line Interface

[![Build Status](https://travis-ci.org/EnlightNS/enlightns-cli.svg?branch=develop)](https://travis-ci.org/EnlightNS/enlightns-cli)

# Installation

- Ubuntu 14.04 or higher

    You need the following libraries

    ```bash
    sudo apt-get install libffi-dev libssl-dev
    ```


# Testing the app clone the repository and activate your virtualenv.
Once it is activated within the repository folder execute the following command line:

    ```bash
    cd enlightns-cli
    pip install --editable .
    ```

Important notice you can test your changes without uninstalling and reinstalling.

# Removing the CLI

    ```bash
    pip uninstall -y enlightns-cli
    ```