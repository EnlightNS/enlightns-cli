# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import click
import netifaces as ni

from enscli.rest.services import EnlightnsApi
from enscli.tools.configurations import EnlightnsConfig
from enscli.tools.interfaces import Device
from enscli.tools.messages import (IF_MSG, SET_REC_MSG, REC_LIST_MSG, REC_FAIL,
                                   REC_WRITE_SUCCESS, SET_IPV6_HELP,
                                   SET_WHICH_IP_HELP, SET_INET_HELP,
                                   SET_DEBUG_HELP, NOTHING_HAPPENED_MSG,
                                   NO_UPDATE, TWO_HELP_MSG, SET_REC_LAN_MSG,
                                   SET_REC_WAN_MSG, REC_OWNER_OR_EXISTS_MSG,
                                   TWO_ONLY_ONE_REC_MSG, TWO_WAY_CFG_MSG,
                                   UPDATE_MSG)


# Click utilities
from enscli.tools.resolver import resolve_a_record

style = click.style

# CLI settings
api = EnlightnsApi()
device = Device()
config = EnlightnsConfig()
gws_ip, interface = ni.gateways()['default'][ni.AF_INET]
if config and config.interface and config.interface in device.interfaces_only():
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
@click.option('-r', '--records', help=SET_REC_MSG)
@click.option('-6', '--ipv6', default='off', type=click.Choice(['on', 'off']),
              help=SET_IPV6_HELP)
@click.option('-w', '--which-ip', default='lan',
              type=click.Choice(['lan', 'wan']), help=SET_WHICH_IP_HELP)
@click.option('-i', '--interface', default=interface,
              type=click.Choice(device.interfaces_only()), help=SET_INET_HELP)
@click.option('-d', '--debug', default='off', type=click.Choice(['on', 'off']),
              help=SET_DEBUG_HELP)
@click.option('-l', '--lan-record', help=SET_REC_LAN_MSG)
@click.option('-p', '--wan-record', help=SET_REC_WAN_MSG)
def configure(records, ipv6, which_ip, interface, debug, lan_record,
              wan_record):
    """Configure the EnlightNS agent."""

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
            rec = ""
            for record in records_list:
                rec = '{' + str(record['id']) + '}' + record['name'] + ','
            config.write('records', rec)
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

    if config.token and (lan_record or wan_record):
        record = lan_record if lan_record else wan_record
        is_local = True if lan_record else False
        if len(record.split(',')) == 1:
            is_owner, record = api.check_records(record=record)
            if is_owner and record:
                cfg = 'record_lan' if is_local else 'record_wan'
                record = '{' + str(record['id']) + '}' + record['name'] + ','
                config.write(cfg, record)
                click.echo(REC_WRITE_SUCCESS)
            else:
                click.echo(REC_OWNER_OR_EXISTS_MSG)
        else:
            click.echo(TWO_ONLY_ONE_REC_MSG)

    if not config.token and (records or lan_record or wan_record):
        click.echo(NOTHING_HAPPENED_MSG)

    return


@cli.command()
def cron():
    """Configure the EnlightNS agent to run through
    a cron"""

    return


@cli.command()
@click.option('-l', '--list-records', default=False, flag_value=True,
              help='List all records available in EnlightNS.com')
@click.option('-a', '--all', default=False, flag_value=True,
              help='List all records including the locally set')
@click.option('-t', '--text', default=False, flag_value=True,
              help='Returns the DNS record in a text format.')
def hosts(list_records, all, text):
    """Manage your DNS record(s)"""

    # Default: show the record that is set in the config file
    if config.records and (not list_records and not text or all):
        click.echo(style('Currently configured record(s) to update:\n', fg='cyan'))
        for record in config.records_to_str():
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
        for record in config.records_to_str():
            click.echo(record)

    if not config.records and not list_records:
        click.echo('Please set a record to update')

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


@cli.command(help=TWO_HELP_MSG)
@click.option('-f', '--force', default=False, flag_value=True,
              help='Force the update of your records.')
@click.option('-s', '--silent', default=False, flag_value=True,
              help='Do not display any output.')
def two(force, silent):

    if config.token and config.record_lan and config.record_wan:
        # Gets LAN and WAN IP addresses
        lan_ip = device.get_ip(config.interface)
        wan_ip = api.ip()
        if 'ip' in wan_ip:
            wan_ip = wan_ip['ip']
        result = []

        if not silent:
            click.echo(UPDATE_MSG)

        # identify the LAN IP address by resolving the record
        pk, record = config.get_record_and_pk(config.record_lan)
        record_ip = resolve_a_record(record)
        record_ip = list(set(record_ip))
        if lan_ip not in record_ip or len(record_ip) > 1 or force:
            result = api.update(pk, lan_ip)

        if result and not silent:
            click.echo(result['name'] + '\t' + result['content'])

        # identify the WAN IP address by resolving the record
        pk, record = config.get_record_and_pk(config.record_wan)
        record_ip = resolve_a_record(record)
        record_ip = list(set(record_ip))
        if wan_ip not in record_ip or len(record_ip) > 1 or force:
            result = api.update(pk, wan_ip)

        if result and not silent:
            click.echo(result['name'] + '\t' + result['content'])
    else:
        click.echo(TWO_WAY_CFG_MSG)

    return


@cli.command()
@click.option('-f', '--force', default=False, flag_value=True,
              help='Force the update of your IP.')
@click.option('-s', '--silent', default=False, flag_value=True,
              help='Do not display any output.')
def update(force, silent):
    """Update your DNS record(s)"""

    # update only if a record is configured and that the client is authenticated
    if config.records and config.token and config.interface and config.which_ip:
        # define which ip to update the record(s) with
        if config.which_ip == 'wan':
            ip = api.ip()
            if 'ip' in ip:
                ip = ip['ip']
        else:
            ip = device.get_ip(config.interface)

        # Get the records
        text_records = config.records_to_str()

        # identify the IP address by resolving the record
        record_ip = []
        for record in text_records:
            record_ip.extend(resolve_a_record(record))
        record_ip = list(set(record_ip))

        # update the record
        if ip not in record_ip or len(record_ip) > 1 or force:
            results = []
            if not silent:
                click.echo(UPDATE_MSG)
                with click.progressbar(config.records_with_pk()) as bar_records:
                    for pk, record in bar_records:
                        result = api.update(pk, ip)
                        if result:
                            results.append(result)

                for r in results:
                    click.echo(r['name'] + '\t' + r['content'])
            else:
                for pk, record in config.records_with_pk():
                    api.update(pk, ip)
        else:
            click.echo(NO_UPDATE) if not silent else None
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
