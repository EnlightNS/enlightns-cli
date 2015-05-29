# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import requests
import json

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
    if config.debug:
        url = ENLIGHTNS_API_DEBUG_URL
    else:
        url = ENLIGHTNS_API_URL
    auth_header = {'Authorization': 'JWT ' + config.token, }

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

    def check_records(self, record):
        """Validates that the record is owned by the user before it can be sets
        in the configuration file.

        :returns: True if the record is owned by the user"""

        url = self.url + '/user/record/{0}/'.format(record)
        headers = self.auth_header

        result = requests.get(url, headers=headers)
        result = result.json() if result.ok else ''

        record = result[0]
        is_owner = True if result and 'name' in result[0] else False

        return is_owner, record

    def update(self):
        """Update the DNS records against the EnlightNS API

        :returns: True if it successfully update the record(s)"""

        url = self.url + '/user/record/{id}/'
        headers = self.auth_header

        # define which ip to update the record(s) with
        if self.config.which_ip == 'wan':
            ip = self.ip()
        else:
            ip = self.device.get_ip(self.config.interface)

        # update the record
        records = self.config.records.split(',')
        records.remove('')
        for record in records:
            id, record = record.split('-')
            result = requests.post(url.format(id=id), data={'content': ip, },
                                   headers=headers)
            result = result.json() if result.ok else False


        # writes the ip to the config file instead of calling the api if it
        # stays the same ip address

        return


