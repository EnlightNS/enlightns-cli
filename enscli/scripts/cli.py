# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import click
import netifaces

from enscli.rest.services import EnlightnsApi
from enscli.tools.configurations import EnlightnsConfig
from enscli.tools.interfaces import Device


# Click utilities
style = click.style

# CLI settings
api = EnlightnsApi()
device = Device()
config = EnlightnsConfig()
ip, interface = netifaces.gateways()['default'][netifaces.AF_INET]
if_msg = """Set which network interface to retrieve the ip from
    Default interface: {0}
    """.format(interface)


@click.group()
@click.version_option(message='%(version)s')
def cli():
    """Helps managing your EnlightNS Dynamic DNS"""
    pass


@cli.command()
@click.option('-u', '--username', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
def authenticate(username, password):
    """Authenticate your account on EnlightNS.com"""
    token = api.authenticate(username=username, password=password)

    if token:
        config.write('token', token)
        click.echo('Successfully authenticated')
    else:
        click.echo('Unable to authenticate your account, please try again.')

    return


@cli.command()
def cron():
    """Configure the EnlightNS agent to run through
    a cron"""

    return


@cli.command()
def interfaces():
    """Displays the available network interfaces on the device."""

    local_interface = device.interfaces()
    click.echo(style('Available interface(s):\n', fg='yellow'))

    for interface in local_interface:
        click.echo('\t- ' + interface)
    click.echo('')

    return


@cli.command()
@click.option('-i', '--interface', default=interface, help=if_msg)
def lan(interface):
    """Returns the LAN IP of the selected device"""
    ip = device.get_ip(interface=interface)
    if ip:
        click.echo(ip)
    else:
        click.echo('Unable to retrieve you local ip address')

    return


@cli.command()
@click.option('-l', '--list-records', default=False, flag_value=True,
              help='List your records')
def records(list_records):
    """Manage your DNS record(s)"""
    # try to connect to the API first if unable to connect you MUST first
    # authenticate
    if config.token and list_records:
        result = api.list_records()
        if result:
            click.echo('Your DNS Records:')
            for record in result:
                click.echo('\t' + record['name'])

    return


@cli.command()
@click.option('-r', '--record', prompt=True, help='The DNS record to update', )
def set():
    """Configure the EnlightNS agent"""

    return


@cli.command()
def update():
    """Update your DNS record(s)"""

    return


@cli.command()
@click.option('-t', '--text', default=False, flag_value=True,
              help='Returns the IP in a text format.')
def wan(text):
    """Returns your public IP"""

    my_ip = api.ip()

    if text and 'ip' in my_ip:
        my_ip = my_ip['ip']

    click.echo(my_ip)

    return
