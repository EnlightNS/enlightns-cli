# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import requests
import json

from enscli.settings import ENLIGHTNS_API_URL
from enscli.tools.configurations import EnlightnsConfig

class EnlightnsApi(object):
    """The class that will encapsulate all the calls we can do to the EnlightNS
    API."""
    url = ENLIGHTNS_API_URL
    config = EnlightnsConfig()
    if config.token:
        token = config.token
    else:
        token = ''
    auth_header = {'Authorization': 'JWT ' + config.token, }

    @classmethod
    def authenticate(self, username, password):
        """Authenticate the user against EnlightNS.com

        :param username: your enlightns.com username
        :param password: your enlightns.com password

        :returns: set the token in the configuration file"""
        url = self.url + '/api-token-auth/'
        headers = {'Content-type': 'application/json'}

        data = {
            'username': username,
            'password': password,
        }

        result = requests.post(url, data=json.dumps(data), headers=headers)
        result = result.json() if result.ok else ''

        if 'token' in result:
            self.token = result['token']

        return self.token

    @classmethod
    def ip(self):
        """Calls the EnlightNS API to get the public IP of the running agent.

        :return: your public IP address.
        """
        url = self.url + '/tools/whatismyip/'

        result = requests.get(url)
        result = result.json() if result.ok else ''

        return result

    def list_records(self):
        """List the DNS records of the user.

        We MUST filter by record type A and AAAA otherwise the CNAME records
        cannot be updated with an IP address.

        :returns: the list of DNS records"""
        url = self.url + '/user/record/?type=A,AAAA'
        headers = self.auth_header

        result = requests.get(url, headers=headers)
        result = result.json() if result.ok else ''

        return result
