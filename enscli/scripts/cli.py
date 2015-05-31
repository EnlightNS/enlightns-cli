# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import click
import netifaces

from enscli.rest.services import EnlightnsApi
from enscli.tools.configurations import EnlightnsConfig
from enscli.tools.interfaces import Device
from enscli.tools.messages import (IF_MSG, SET_REC_MSG, REC_LIST_MSG, REC_FAIL,
                                   REC_WRITE_SUCCESS, SET_IPV6_HELP,
                                   SET_WHICH_IP_HELP, SET_INET_HELP,
                                   SET_DEBUG_HELP, NOTHING_HAPPENED_MSG)


# Click utilities
style = click.style

# CLI settings
api = EnlightnsApi()
device = Device()
config = EnlightnsConfig()
ip, interface = netifaces.gateways()['default'][netifaces.AF_INET]
if config and config.interface:
    interface = config.interface


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

    for inet, ip in local_interface.items():
        msg = '\t' + inet.ljust(10, str(' '))
        if ip and 'ipv4' in ip:
            ipv4 = str(ip['ipv4'])
            msg += 'IPv4: ' + ipv4.ljust(16, str(' '))
        if ip and 'ipv6' in ip:
            msg += 'IPv6: ' + ip['ipv6']
        click.echo(msg)
    click.echo('')

    return


@cli.command()
@click.option('-i', '--interface', default=interface,
              type=click.Choice(device.interfaces_only()),
              help=IF_MSG.format(interface))
def lan(interface):
    """Returns the LAN IP of the selected device"""

    ip = device.get_ip(interface=interface)
    if ip:
        click.echo(ip)
    else:
        click.echo('Unable to retrieve you local ip address')

    return


@cli.command()
def logout():
    """Logout your account from the agent."""
    config.write('token', '')
    click.echo('You successfully logged out.')

    return


@cli.command()
@click.option('-l', '--list-records', default=False, flag_value=True,
              help='List all records available in EnlightNS.com')
@click.option('-a', '--all', default=False, flag_value=True,
              help='List all records including the locally set')
@click.option('-t', '--text', default=False, flag_value=True,
              help='Returns the DNS record in a text format.')
def records(list_records, all, text):
    """Manage your DNS record(s)"""

    # Default: show the record that is set in the config file
    if config.records and (not list_records and not text or all):
        click.echo(style('Currently configured record(s) to update:\n', fg='cyan'))
        records_list = config.records.split(',')
        records_list.remove('')
        for record in records_list:
            pk, record = record.split('}')
            click.echo('\t' + record)
        click.echo('')

    # list the records from the API
    if config.token and list_records or all:
        result = api.list_records()
        if result:
            click.echo(style('Your DNS Records:\n', fg='yellow'))
            for record in result:
                click.echo(
                    REC_LIST_MSG.format(record['name'],
                                        str(record['ttl']).ljust(6, str(' ')),
                                        record['content'].ljust(15, str(' ')),
                                        record['type']))
            click.echo('')

    if text and not all and not list_records:
        records_list = config.records.split(',')
        records_list.remove('')
        for record in records_list:
            pk, record = record.split('}')
            click.echo(record)

    if not config.records and not list_records:
        click.echo('Please set a record to update')

    return


@cli.command()
@click.option('-r', '--records', help=SET_REC_MSG)
@click.option('-6', '--ipv6', default='off', type=click.Choice(['on', 'off']),
              help=SET_IPV6_HELP)
@click.option('-w', '--which-ip', default='lan',
              type=click.Choice(['lan', 'wan']), help=SET_WHICH_IP_HELP)
@click.option('-i', '--interface', default=interface,
              type=click.Choice(device.interfaces_only()), help=SET_INET_HELP)
@click.option('-d', '--debug', default='off', type=click.Choice(['on', 'off']),
              help=SET_DEBUG_HELP)
def set(records, ipv6, which_ip, interface, debug):
    """Configure the EnlightNS agent"""

    # validates ownership of the record(s)
    if config.token and records:
        valid_list = []
        records_list = []
        click.echo('Validating the records ...')
        with click.progressbar(records.split(',')) as prompt_records:
            for record in prompt_records:
                is_owner, record = api.check_records(record=record)
                valid_list.append(is_owner)
                records_list.append(record)

        if False in valid_list:
            click.echo(REC_FAIL)
        else:
            # Write the records to the configuration file
            record_config = ""
            for record in records_list:
                record_config += '{' + str(record['id']) + '}' + record['name'] + ','
            config.write('records', record_config)
            click.echo(REC_WRITE_SUCCESS)

    # set if IPv6 is supported
    if ipv6:
        config.write('ipv6', ipv6)

    # set if we update the record with the public or local ip address
    if which_ip:
        config.write('which_ip', which_ip)

    # set the interface we get the ip address from
    if interface:
        config.write('interface', interface)

    # set the debug on
    if debug:
        config.write('debug', debug)

    return


@cli.command()
@click.option('-f', '--force', default=False, flag_value=True,
              help='Force the update of your IP.')
def update(force):
    """Update your DNS record(s)"""

    # update only if a record is set to update and that the client is
    # authenticated
    if config.records and config.token and config.interface and config.which_ip:
        # define which ip to update the record(s) with
        if config.which_ip == 'wan':
            ip = api.ip()
            if 'ip' in ip:
                ip = ip['ip']
        else:
            ip = device.get_ip(config.interface)

        if (not config.known_ip or ip != config.known_ip) or force:
            # update the record
            records = config.records.split(',')
            records.remove('')
            results = []
            click.echo('Updating the record(s) ...')
            with click.progressbar(records) as update_records:
                for record in update_records:
                    pk, record = record.split('}')
                    pk = pk[1:]
                    result = api.update(pk, ip)
                    if result:
                        results.append(result)

            for r in results:
                click.echo(r['name'] + '\t' + r['content'])
        else:
            # TODO: implement a resolver
            click.echo('No update needed')

        config.write('known_ip', ip)
    else:
        click.echo(NOTHING_HAPPENED_MSG)

    return


@cli.command()
@click.option('-j', '--json', default=False, flag_value=True,
              help='Returns the IP in a JSON format.')
def wan(json):
    """Returns your public IP"""

    my_ip = api.ip()

    if not(json and 'ip' in my_ip):
        my_ip = my_ip['ip']

    click.echo(my_ip)

    return
