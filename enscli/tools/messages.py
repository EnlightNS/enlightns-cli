# -*- coding: utf-8 -*-
"""
This module contains the 

"""
from __future__ import unicode_literals, absolute_import

# Help Messages
IF_MSG = """Set the network interface to retrieve the ip
    Default interface: {0}
    """
SET_REC_MSG = """Set the record(s) to update
    example:
        "test.enlightns.com" or "test.enlightns.com,test2.enlightns.com"
    """
REC_LIST_MSG = "\t{0}\tTTL: {1} IP: {2} TYPE: {3}"
REC_FAIL = """You are not the owner of the record or it does not exists"""
REC_WRITE_SUCCESS = """Successfully wrote the record(s) to your configuration file."""
SET_IPV6_HELP = """Set to use IPv6 address"""
SET_WHICH_IP_HELP = """Set which IP it will use to update the DNS record"""
SET_INET_HELP = """Set which interface to use for the updates"""
SET_DEBUG_HELP = """Turn on|off debug"""
NOTHING_HAPPENED_MSG = """Did you authenticate the agent? or Is it well configured?"""
NO_UPDATE = """No update needed."""