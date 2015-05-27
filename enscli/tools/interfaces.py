# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import netifaces

class Device(object):
    """Represents the device where the CLI is executed."""

    @classmethod
    def interfaces(self):
        """Returs the network interfaces of the device or computer."""
        local_interfaces = netifaces.interfaces()
        local_interfaces.remove('lo')
        return local_interfaces
