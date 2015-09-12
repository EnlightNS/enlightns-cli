# -*- coding: utf-8 -*-
from __future__ import absolute_import

from dns.resolver import Resolver
import dns.rdatatype

from enscli.settings import GOOGLE_NAMESERVERS


def resolve_a_record(hostname, nameservers=GOOGLE_NAMESERVERS):
    """This function open a connection to a DNS resolver and then tries to
    resolve the IP address of your record. Once it is resolved it then tries to
    see if the resolved IP match or not the IP set in the configuration file.

    :param hostname: the record name to resolve
    :param nameservers: the nameservers where to resolve the record

    :returns: the IP address the record has been resolved to"""
    infos = []
    try:
        resolver = Resolver(configure=False)
        resolver.nameservers = nameservers

        # First get the NS record to know which server to query
        domain = ".".join(hostname.split('.')[-2:])
        resolution = resolver.query(qname=domain, rdtype=dns.rdatatype.NS)
        nameservers_name = []
        for ns_record in resolution.rrset.items:
            nameservers_name.append(ns_record.to_text())

        # Get the A record IP address of the NS records
        ns_ips = []
        for ns_record in nameservers_name:
            resolution = resolver.query(ns_record)
            for ip in resolution.rrset.items:
                ns_ips.append(ip.address)
        ns_ips = list(set(ns_ips))

        # Resolve the IP of the record
        resolver.nameservers = ns_ips
        resolution = resolver.query(hostname)
        for ip in resolution.rrset.items:
            infos.append(ip.address)
    except:
        pass

    # this should return only a single IP address if all DNS servers are in sync
    return infos


def get_record_ttl(record, nameservers=GOOGLE_NAMESERVERS):
    """This function returns the TTL of a record after it resolved it using a
    DNS resolver.

    :param record: the record to resolve

    :returns: the TTL of the record
    """
    ttl = False
    # try:
    resolver = Resolver(configure=False)
    resolver.nameservers = nameservers
    resolution = resolver.query(record)
    ttl = resolution.rrset.ttl
    # except:
    #     pass

    return ttl
