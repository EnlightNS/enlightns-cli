# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import requests
import json

from enscli.settings import ENLIGHTNS_API_URL

class EnlightnsApi(object):
    """The class that will encapsulate all the calls we can do to the EnlightNS
    API."""
    url = ENLIGHTNS_API_URL

    @classmethod
    def ip(self):
        """Calls the EnlightNS API to get the public IP of the running agent.

        :return: your public IP address.
        """
        url = self.url + '/tools/whatismyip/'
        result = requests.get(url)

        return json.loads(result.content)


