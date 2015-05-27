# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import click

from enscli.rest.services import EnlightnsApi
from enscli.tools.interfaces import Device

api = EnlightnsApi()
device = Device()


@click.group()
@click.version_option(message='%(version)s')
def cli():
    """Helps creating the database"""
    pass


@cli.command()
def interfaces():
    """Displays the available network interfaces on the device."""
    local_interface = device.interfaces()
    click.echo(click.style('Available interface(s):', fg='green'))
    for interface in local_interface:
        click.echo('\t' + interface)


@cli.command()
@click.option('-t', '--text', default=False, flag_value=True, help='Returns the IP in a text format.')
def whatismyip(text):
    """Retrieves your public IP from the EnlightNS REST Service."""
    my_ip = api.ip()

    if text and 'ip' in my_ip:
        my_ip = my_ip['ip']

    click.echo(my_ip)
