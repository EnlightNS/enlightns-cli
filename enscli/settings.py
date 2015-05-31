# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os

ENLIGHTNS_API_URL = 'http://devapi.enlightns.com'
ENLIGHTNS_API_DEBUG_URL = 'http://127.0.0.1:8000'
ENLIGHTNS_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENLIGHTNS_CONFIG_DIR = ENLIGHTNS_BASE_DIR + '/.enlightns'
ENLIGHTNS_CONFIG_FILE = 'enlightns.conf'
ENLIGHTNS_CONFIG_FULLPATH = ENLIGHTNS_CONFIG_DIR + '/' + ENLIGHTNS_CONFIG_FILE
ENLIGHTNS_CONFIG_SECTION = 'enlightns'

GOOGLE_NAMESERVERS = ['8.8.8.8', '8.8.4.4', ]

