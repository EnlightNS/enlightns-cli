# -*- coding: utf-8 -*-
from __future__ import absolute_import

from click.testing import CliRunner
import pytest


@pytest.fixture(scope='function')
def runner(request):
    return CliRunner()

