# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os


ENLIGHTNS_API_URL = 'https://api.enlightns.com'
ENLIGHTNS_API_DEBUG_URL = 'http://127.0.0.1:8000'
ENLIGHTNS_BASE_DIR = os.path.expanduser("~")
ENLIGHTNS_CONFIG_DIR = ENLIGHTNS_BASE_DIR + '/.enlightns'
ENLIGHTNS_CONFIG_FILE = 'enlightns.conf'
ENLIGHTNS_CONFIG_FULLPATH = ENLIGHTNS_CONFIG_DIR + '/' + ENLIGHTNS_CONFIG_FILE
ENLIGHTNS_CONFIG_SECTION = 'enlightns'

GOOGLE_NAMESERVERS = ['8.8.8.8', '8.8.4.4', ]

