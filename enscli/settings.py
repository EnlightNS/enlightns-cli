# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os

ENLIGHTNS_API_URL = 'http://devapi.enlightns.com'
ENLIGHTNS_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENLIGHTNS_CONFIG_DIR = ENLIGHTNS_BASE_DIR + '/.enlightns'
ENLIGHTNS_CONFIG_FILE = 'enlightns.conf'
ENLIGHTNS_CONFIG_FULLPATH = ENLIGHTNS_CONFIG_DIR + '/' + ENLIGHTNS_CONFIG_FILE
ENLIGHTNS_CONFIG_SECTION = 'enlightns'
