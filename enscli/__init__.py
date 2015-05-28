# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

"""This is the main file to run the EnlightNS CLI. """

import os

from enscli.settings import (ENLIGHTNS_BASE_DIR, ENLIGHTNS_CONFIG_DIR,
                             ENLIGHTNS_CONFIG_FULLPATH,)

__version__ = '0.0.1'

mode = '0600'
mode_int = 0600

# Create the setting folder if it does not exists
if not os.path.exists(ENLIGHTNS_CONFIG_DIR):
    os.makedirs(ENLIGHTNS_CONFIG_DIR, mode=mode)

# Create the configuration file if it does not exists
if not os.path.isfile(ENLIGHTNS_CONFIG_FULLPATH):
    file = os.fdopen(
        os.open(ENLIGHTNS_CONFIG_FULLPATH, os.O_WRONLY | os.O_CREAT, mode_int),
        'w+'
    )
    file.close()


