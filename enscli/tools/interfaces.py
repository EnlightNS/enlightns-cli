# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import netifaces

class Device(object):
    """Represents the device where the CLI is executed."""

    @classmethod
    def interfaces(self):
        """Returns the network interfaces of the device or computer.

        :returns: the available network interfaces """
        local_interfaces = netifaces.interfaces()
        return local_interfaces

    def get_ip(self, interface):
        """Returns the ip address of the selected network interface.

        :returns: the ip address """
        try:
            lan_ip = netifaces.ifaddresses(interface)[netifaces.AF_INET].pop()[
                'addr'].strip()
        except Exception, e:
            lan_ip = ''

        return lan_ip
