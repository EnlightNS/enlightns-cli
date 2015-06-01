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
SET_REC_LAN_MSG = """Set the LAN record (Two way mode)."""
SET_REC_WAN_MSG = """Set the WAN record (Two way mode)."""
REC_LIST_MSG = "\t{0}\tTTL: {1} IP: {2} TYPE: {3}"
REC_FAIL = """You are not the owner of the record or it does not exists"""
REC_WRITE_SUCCESS = """Successfully wrote the record(s) to your configuration file."""
SET_IPV6_HELP = """Set to use IPv6 address"""
SET_WHICH_IP_HELP = """Set which IP it will use to update the DNS record"""
SET_INET_HELP = """Set which interface to use for the updates"""
SET_DEBUG_HELP = """Turn on|off debug"""
NOTHING_HAPPENED_MSG = """Did you authenticate the agent? or Is it well configured?"""
NO_UPDATE = """No update needed."""
TWO_ONLY_ONE_REC_MSG = """You can only use one DNS record using the Two way mode."""
TWO_HELP_MSG = """Two way update mode.

Using this mode you can update to two different DNS
records your public and local IP addresses.

You MUST configure the WAN and LAN records.

Example:

    Public  wan.enlightns.com --> 24.85.96.58

    Local   lan.enlightns.com --> 192.168.1.100
"""
REC_OWNER_OR_EXISTS_MSG = """Please validate that the record belongs to you or that it exists."""
TWO_WAY_CFG_MSG = """You MUST configure the LAN and WAN records."""
UPDATE_MSG = """Updating the record(s) ..."""
