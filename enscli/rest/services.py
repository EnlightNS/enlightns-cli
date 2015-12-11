# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json

import requests

from enscli.settings import ENLIGHTNS_API_URL, ENLIGHTNS_API_DEBUG_URL
from enscli.tools.configurations import EnlightnsConfig
from enscli.tools.interfaces import Device


class EnlightnsApi(object):
    """The class that will encapsulate all the calls we can do to the EnlightNS
    API."""
    config = EnlightnsConfig()
    if config.token:
        token = config.token
    else:
        token = ''
    device = Device()
    if config.debug == "on":
        url = ENLIGHTNS_API_DEBUG_URL
    else:
        url = ENLIGHTNS_API_URL
    auth_header = {'Authorization': config.token, }

    def authenticate(self, email, password):
        """Authenticate the user against EnlightNS.com

        :param email: your enlightns.com username
        :param password: your enlightns.com password

        :returns: set the token in the configuration file"""
        url = self.url + '/api-token-auth/'
        headers = {'Content-type': 'application/json'}

        data = {
            'email': email,
            'password': password,
        }

        result = requests.post(url, data=json.dumps(data), headers=headers)
        result = result.json() if result.ok else ''

        if 'token' in result:
            self.token = result['token']

        return self.token

    def ip(self):
        """Calls the EnlightNS API to get the public IP of the running agent.

        :return: your public IP address.
        """
        url = self.url + '/tools/whatismyip/'

        result = requests.get(url)
        result = result.json() if result.ok else ''

        return result

    def get_ttls(self):
        """Calls the EnlightNS API to get the TTLs of the account. It will help
        setup the cron.

        :return: a TTL list.
        """
        url = self.url + '/user/ttl/'
        headers = self.auth_header

        result = requests.get(url, headers=headers)
        result = result.json() if result.ok else ''

        ttl_str = ''
        if result:
            for ttl in result:
                ttl_str += str(ttl['seconds']) + ', '

        return ttl_str[:-2]

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

    def check_records(self, record):
        """Validates that the record is owned by the user before it can be sets
        in the configuration file.

        :returns: True if the record is owned by the user"""

        url = self.url + '/user/record/{0}/'.format(record)
        headers = self.auth_header

        result = requests.get(url, headers=headers)
        result = result.json() if result.ok else ''

        try:
            record = result[0]
            is_owner = True if result and 'name' in result[0] else False
        except Exception, e:
            record = None
            is_owner = False

        return is_owner, record

    def update(self, pk, ip):
        """Update the DNS records against the EnlightNS API

        :returns: True if it successfully update the record(s)"""

        url = self.url + '/user/record/{pk}/'.format(pk=pk)
        headers = self.auth_header

        result = requests.put(url, data={'content': ip, }, headers=headers)

        return result.json() if result.ok else False
