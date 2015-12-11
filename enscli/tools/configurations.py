# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ConfigParser import ConfigParser
import shutil

import click

from enscli.settings import (ENLIGHTNS_CONFIG_FULLPATH,
                             ENLIGHTNS_CONFIG_SECTION, 
                             ENLIGHTNS_CONFIG_DIR, )


class EnlightnsConfig(object):
    """Class to configure the EnlightNS CLI

    it stores the configuration into a INI style file located at

    .enlightns/enlightns.conf

    example:

        [enlightns]
        # enlightns api token
        token = t8otffvsmhjloexa9so3e1vp2lixh1ihghtt3hhezaflee54dstgow0luyh...

        # a single record or a list of records
        # test.enlightns.com
        # or
        # test.enlightns.com,test2.enlightns.com
        records = test.enlightns.com

        # interface possible values [en0, eth0, wlan0, etc]
        interface = eth0

        # which_ip possible values (wan|lan)
        which_ip = lan

        #set if we update using IPv6 (on|off)
        ipv6 = on
    """
    config = {}
    token = ''
    records = []
    record_wan = ''
    record_lan = ''
    interface = ''
    which_ip = ''
    ipv6 = ''
    known_ip = ''
    debug = ''

    def __init__(self):
        # Read the configuration file
        self.config = self.read()

        if 'token' in self.config:
            self.token = self.config['token']

        if 'records' in self.config:
            self.records = self.config['records']

        if 'record_wan' in self.config:
            self.record_wan = self.config['record_wan']

        if 'record_lan' in self.config:
            self.record_lan = self.config['record_lan']

        if 'interface' in self.config:
            self.interface = self.config['interface']

        if 'which_ip' in self.config:
            self.which_ip = self.config['which_ip']

        if 'ipv6' in self.config:
            self.ipv6 = self.config['ipv6']

        if 'known_ip' in self.config:
            self.known_ip = self.config['known_ip']

        if 'debug' in self.config:
            self.debug = self.config['debug']

    @staticmethod
    def read():
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

    @staticmethod
    def write(option, value):
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

    def records_to_str(self):
        """Returns the configured records into a list of string"""
        records = self.records.split(',')
        records.remove('')
        text_records = []
        for record in records:
            text_records.append(self.record_to_str(record))

        return text_records

    @staticmethod
    def record_to_str(record):
        """Returns the configured records into a list of string"""
        record = record.split(',')
        try:
            record.remove('')
        except ValueError:
            pass
        pk, record = record[0].split('}')

        return record

    def records_with_pk(self):
        """Returns the configured records into a list made of tuple:

        [(pk, hostname), (pk, hostname)]
        """
        records = self.records.split(',')
        records.remove('')
        records_list = []
        for record in records:
            pk, record = record.split('}')
            pk = pk[1:]
            records_list.append((pk, record))

        return records_list

    @staticmethod
    def get_record_and_pk(record):
        """Returns the LAN or WAN record from the configuration file.

        :param record: the record to extract the pk and record

        :returns: the pk and the record
        """

        record = record.split(',')
        record.remove('')
        pk, record = record[0].split('}')
        pk = pk[1:]

        return pk, record

    @staticmethod
    def logout():
        """Deletes the configuration file"""
        try:
            shutil.rmtree(ENLIGHTNS_CONFIG_DIR, ignore_errors=True)
        except Exception, e:
            msg = 'Unable to delete the configuration file, error: {0}'
            click.echo(click.style(msg.format(e), fg='red'))


