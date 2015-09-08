# -*- coding: utf-8 -*-
from __future__ import absolute_import

import netifaces as ni
from IPy import IP

from enscli.tools.configurations import EnlightnsConfig

class Device(object):
    """Represents the device where the CLI is executed."""

    config = EnlightnsConfig()

    @classmethod
    def interfaces_only(self):
        """Returns the network interfaces of the device or computer.

        :returns: the available network interfaces """
        local_interfaces = ni.interfaces()
        return local_interfaces

    @classmethod
    def interfaces(self):
        """Returns the network interfaces and its IP address of the device or
        computer.

        :returns: the available network interfaces and its ip address."""
        local_interfaces = ni.interfaces()
        inet_and_ip = {}
        for inet in local_interfaces:
            inet_and_ip[inet] = {}
            try:
                ipv4 = ni.ifaddresses(inet)[ni.AF_INET][0]['addr']
                inet_and_ip[inet]['ipv4'] = ipv4
            except:
                inet_and_ip[inet]['ipv4'] = ''
            try:
                ipv6 = ni.ifaddresses(inet)[ni.AF_INET6][0]['addr']
                inet_and_ip[inet]['ipv6'] = ipv6
            except:
                inet_and_ip[inet]['ipv6'] = ''

        return inet_and_ip

    def get_ip(self, interface):
        """Returns the ip address of the selected network interface.

        :param interface: the network interface

        :returns: the ip address """
        if self.config.ipv6 and self.config.ipv6 == 'on':
            inet = ni.AF_INET6
        else:
            inet = ni.AF_INET

        try:
            lan_ip = ni.ifaddresses(interface)[inet][0]['addr'].strip()
            # on a mac the IPv6 is followed by %interface_name
            # in my case it was %en5 had to clean this out
            lan_ip = lan_ip.split('%')[0]
            IP(lan_ip)
        except Exception, e:
            lan_ip = False

        if not lan_ip:
            # We don't care about this local ip it is the gateway ip
            gws_ip, inet = ni.gateways()['default'][ni.AF_INET]
            try:
                if self.config.ipv6 == 'off':
                    lan_ip = ni.ifaddresses(inet)[ni.AF_INET][0]['addr']
                    IP(lan_ip)
                else:
                    lan_ip = ni.ifaddresses(inet)[ni.AF_INET6][0]['addr']
                    IP(lan_ip)
            except Exception, e:
                lan_ip = False

        return lan_ip
