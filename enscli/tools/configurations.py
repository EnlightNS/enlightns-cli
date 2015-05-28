# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from ConfigParser import ConfigParser

from enscli.settings import (ENLIGHTNS_CONFIG_FULLPATH,
                             ENLIGHTNS_CONFIG_SECTION, )


class EnlightnsConfig(object):
    """Class to configure the EnlightNS CLI

    it stores the configuration into a INI style file located at

    .enlightns/enlightns.conf

    example:

        [enlightns]
        # enlightns api token
        token=t8otffvsmhjloexa9so3e1vp2lixh1ihghtt3hhezaflee54dstgow0luyhetc33oi9hfoqbpsp6rsxjam3ns4yfdfh06rujutxo1yktytymni3hnsg5elmv29dxo04emhxz0whhdswj3bfckaikdrwvolb5aqir0rcvapwkng3ult6fej3xfmh56vn4tld0v0ir34hjrj6q7e4mwud41qfx04ohpcqhmtmr

        # a single record or a list of records
        # test.enlightns.com
        # or
        # test.enlightns.com,test2.enlightns.com
        records=test.enlightns.com

        # interface possible values [en0, eth0, wlan0, etc]
        interface=eth0

        # which_ip possible values [wan, lan]
        which_ip=lan
    """
    config = {}
    token = ''
    records = []
    interface = ''
    which_ip = ''

    def __init__(self):
        # Read the configuration file
        self.config = self.read()

        if 'token' in self.config:
            self.token = self.config['token']

        if 'records' in self.config:
            self.records = self.config['records']

        if 'interface' in self.config:
            self.interface = self.config['interface']

        if 'which_ip' in self.config:
            self.which_ip = self.config['which_ip']

    def read(self):
        '''This function load all the configurations from the file located in
        .enlightns/enlightns.conf and return all the information.

        :returns: the configurations of the EnlightNS agent
        '''

        config = ConfigParser()
        config.read(ENLIGHTNS_CONFIG_FULLPATH)

        sections = config.sections()

        options = []

        for s in sections:
            options.extend(config.items(s))

        configs = {}

        for key, value in options:
            configs[key] = value

        return configs

    def write(self, option, value):
        """Sets the option=value in the configuration file

        :param option: the name of the option
        :param value: the value of the option

        :returns: true if written"""

        section = ENLIGHTNS_CONFIG_SECTION
        config = ConfigParser()
        config.read(ENLIGHTNS_CONFIG_FULLPATH)

        if not config.has_section(section):
            config.add_section(section)

        with open(ENLIGHTNS_CONFIG_FULLPATH, "w+") as file:
            config.set(section, option, value)
            config.write(file)

        return option, value

