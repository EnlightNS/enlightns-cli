# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

import click
import netifaces as ni

from enscli.rest.services import EnlightnsApi
from enscli.tools.configurations import EnlightnsConfig
from enscli.tools.cron import create_a_cron
from enscli.tools.exceptions import EnlightnsException
from enscli.tools.interfaces import Device
from enscli.tools.messages import (IF_MSG, SET_REC_MSG, REC_LIST_MSG, REC_FAIL,
                                   REC_WRITE_SUCCESS, SET_IPV6_HELP,
                                   SET_WHICH_IP_HELP, SET_INET_HELP,
                                   SET_DEBUG_HELP, NOTHING_HAPPENED_MSG,
                                   NO_UPDATE, TWO_HELP_MSG, SET_REC_LAN_MSG,
                                   SET_REC_WAN_MSG, REC_OWNER_OR_EXISTS_MSG,
                                   TWO_ONLY_ONE_REC_MSG, TWO_WAY_CFG_MSG,
                                   UPDATE_MSG, CRON_TWO_MSG, CRON_STD_MSG,
                                   CRON_TWO_WRITTEN_MSG, CRON_STD_WRITTEN_MSG,
                                   CRON_EXISTS, REC_NOT_AVAIL, CFG_RECORDS_MSG,
                                   CFG_TWO_WAY_RECORDS, CFG_API_AVAIL_RECORDS,
                                   AUTHENTICATE_MSG, CANNOT_AUTHENTICATE, SHOW_CONFIG_HELP)
from enscli.tools.resolver import resolve_a_record


# Click utilities
style = click.style

# CLI settings
api = EnlightnsApi()
device = Device()
config = EnlightnsConfig()
try:
    gws_ip, inet = ni.gateways()['default'][ni.AF_INET]
    if config and config.interface:
        inet = config.interface
except KeyError, e:
    # No default gateway happens on Linux containers
    inet = ''


@click.group()
@click.version_option(message='%(version)s')
def cli():
    """Helps managing your EnlightNS Dynamic DNS"""


@cli.command()
@click.option('-e', '--email', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
def authenticate(email, password):
    """Authenticate your account on EnlightNS.com"""
    token = api.authenticate(email=email, password=password)

    if not token:
        raise EnlightnsException(CANNOT_AUTHENTICATE)
    else:
        config.write('token', token)
        click.echo('Successfully authenticated')

    return


@cli.command()
def bash():
    """\b
    Bash auto-completion functionality.
    To install the bash completion execute the two following command lines:
    \b
    enlightns-cli bash >> ~/.bashrc
    source ~/.bashrc
    """
    #
    # GENERATING THIS FILE
    # _ENLIGHTNS_CLI_COMPLETE=source enlightns-cli > bash-complete.sh
    #
    BASE_PATH = os.path.dirname(__file__)
    file_path = os.path.join(BASE_PATH, 'bash_complete.sh')

    with open(file_path) as f:
        click.echo(f.read())

    return



@cli.command()
@click.option('-t', '--two-way', default=False, flag_value=True,
              help='Set cron for the two way update mode.')
@click.option('-a', '--agent', default=False, flag_value=True,
              help='Set cron for the standard update mode.')
@click.option('-s', '--show', default=False, flag_value=True,
              help='Show the written cron.')
def cron(two_way, agent, show):
    """Configure the EnlightNS agent to run through a cron"""

    new_cron = False
    is_written = False

    if not config.token:
        raise EnlightnsException(AUTHENTICATE_MSG)

    if two_way and not (config.record_lan or config.record_wan):
        raise EnlightnsException(TWO_WAY_CFG_MSG)

    if agent and not config.records:
        raise EnlightnsException(REC_NOT_AVAIL)

    if not agent and not two_way:
        click.echo('Please choose which cron you want to write.')
        raise EnlightnsException('enlightns-cli cron --help')

    if two_way:
        # using the first record to get the TTL therefore the update schedule
        pk, record = config.get_record_and_pk(config.record_lan)
        wan_pk, wan_record = config.get_record_and_pk(config.record_wan)
        is_owner, rec = api.check_records(record)
        w_is_owner, w_rec = api.check_records(wan_record)
        if rec and w_rec and is_owner:
            ttl = rec['ttl'] if rec['ttl'] <= w_rec['ttl'] else w_rec['ttl']
            is_written, new_cron = create_a_cron(ttl, action='two',
                                            comment=CRON_TWO_MSG)

        if is_written:
            click.echo(CRON_TWO_WRITTEN_MSG)
        else:
            click.echo(CRON_EXISTS)

    if agent:
        record = config.records_to_str()[0]
        is_owner, rec = api.check_records(record)
        if rec and is_owner:
            is_written, new_cron = create_a_cron(rec['ttl'], action='update',
                                             comment=CRON_STD_MSG)

        if is_written:
            click.echo(CRON_STD_WRITTEN_MSG)
        else:
            click.echo(CRON_EXISTS)

    if show and is_written and new_cron:
        new_cron = new_cron.strip().split('\n')
        try:
            new_cron.remove('')
        except:
            pass
        for tab in new_cron:
            click.echo(tab)

    return


@cli.command()
@click.option('-l', '--list-records', default=False, flag_value=True,
              help='List all records available in EnlightNS.com')
@click.option('-a', '--all', default=False, flag_value=True,
              help='List all records including the locally set')
@click.option('-t', '--text', default=False, flag_value=True,
              help='Returns the DNS record in a text format. (use alone)')
def hosts(list_records, all, text):
    """Manage your DNS record(s)"""
    if not config.token:
        raise EnlightnsException(AUTHENTICATE_MSG)

    # Default: show the record that is set in the config file
    if config.records and (not list_records and not text or all):
        click.echo(style(CFG_RECORDS_MSG, fg='cyan'))
        for record in config.records_to_str():
            click.echo('\t' + record)
        click.echo('')

    # show lan and wan record if they are set
    if not text and not list_records and all and (config.record_lan
                                                  and config.record_wan):
        click.echo(style(CFG_TWO_WAY_RECORDS, fg='green'))

        if config.record_lan:
            click.echo('\t' + config.record_to_str(config.record_lan))

        if config.record_wan:
            click.echo('\t' + config.record_to_str(config.record_wan))
        click.echo('')

    # list the records from the API
    if list_records or all:
        result = api.list_records()
        if result:
            click.echo(style(CFG_API_AVAIL_RECORDS, fg='yellow'))
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
@click.option('-i', '--interface', type=click.Choice(device.interfaces_only()),
              help=IF_MSG.format(inet))
def lan(interface):
    """Returns the LAN IP of the selected device"""
    if not interface and not config.interface:
        raise EnlightnsException(SET_INET_HELP)

    if interface:
        ip = device.get_ip(interface=interface)
    else:
        ip = device.get_ip(interface=config.interface)

    if ip:
        click.echo(ip)
    else:
        click.echo('Unable to retrieve your local ip address')

    return


@cli.command()
def logout():
    """Logout your account from the agent."""
    config.logout()
    click.echo('You successfully logged out.')
    return


@cli.command()
@click.option('-s', '--show', default=False, flag_value=True, help=SHOW_CONFIG_HELP)
@click.option('-r', '--records', help=SET_REC_MSG)
@click.option('-6', '--ipv6', type=click.Choice(['on', 'off']),
              help=SET_IPV6_HELP)
@click.option('-w', '--which-ip', type=click.Choice(['lan', 'wan']),
              help=SET_WHICH_IP_HELP)
@click.option('-i', '--interface', type=click.Choice(device.interfaces_only()),
              help=SET_INET_HELP)
@click.option('-d', '--debug', type=click.Choice(['on', 'off']),
              help=SET_DEBUG_HELP)
@click.option('-l', '--lan-record', help=SET_REC_LAN_MSG)
@click.option('-p', '--wan-record', help=SET_REC_WAN_MSG)
def setup(show, records, ipv6, which_ip, interface, debug, lan_record,
          wan_record):
    """Setup the EnlightNS agent."""
    if show:
        for key, value in config.read().items():
            if not key == "token":
                if key in ['record_lan', 'record_wan']:
                    value = config.record_to_str(value)
                if key in ['records']:
                    value = ', '.join(config.records_to_str())
                click.echo("{}: {}".format(key, value))
        return

    if not config.token:
        raise EnlightnsException(AUTHENTICATE_MSG)

    if not (records or ipv6 or which_ip or interface or debug or lan_record or
            wan_record):
        raise EnlightnsException("enlightns-cli setup --help")

    # validates ownership of the record(s)
    if records:
        valid_list = []
        records_list = []
        click.echo('Validating the records ...')
        with click.progressbar(records.split(',')) as prompt_records:
            for record in prompt_records:
                is_owner, record = api.check_records(record=record)
                valid_list.append(is_owner)
                records_list.append(record)

        if False in valid_list:
            raise EnlightnsException(REC_FAIL)
        else:
            # Write the records to the configuration file
            rec = ""
            for record in records_list:
                rec += '{' + str(record['id']) + '}' + record['name'] + ','
            config.write('records', rec)
            click.echo(REC_WRITE_SUCCESS.format(records))

    # set if IPv6 is supported
    if ipv6:
        config.write('ipv6', ipv6)
    elif not ipv6 and not config.ipv6:
        config.write('ipv6', 'off')

    # set if we update the record with the public or local ip address
    if which_ip in ['wan', 'lan']:
        config.write('which_ip', which_ip)
    elif not which_ip and not config.which_ip:
        config.write('which_ip', 'lan')

    # set the interface we get the ip address from
    if interface:
        config.write('interface', interface)
    elif not interface and not config.interface:
        config.write('interface', inet)

    # set the debug on
    if debug:
        config.write('debug', debug)
    elif not debug and not config.debug:
        config.write('debug', 'off')

    # sets the lan record for two way mode
    if lan_record and not len(lan_record.split(',')) == 1:
        raise EnlightnsException(TWO_ONLY_ONE_REC_MSG)

    if lan_record and len(lan_record.split(',')) == 1:
        is_owner, record = api.check_records(record=lan_record)
        if not (is_owner and record):
            raise EnlightnsException(REC_OWNER_OR_EXISTS_MSG)
        else:
            record = '{' + str(record['id']) + '}' + record['name'] + ','
            config.write('record_lan', record)
            click.echo(REC_WRITE_SUCCESS.format('LAN'))

    # sets the wan record for two way mode
    if wan_record and not len(wan_record.split(',')) == 1:
        raise EnlightnsException(TWO_ONLY_ONE_REC_MSG)

    if wan_record and len(wan_record.split(',')) == 1:
        is_owner, record = api.check_records(record=wan_record)
        if not (is_owner and record):
            raise EnlightnsException(REC_OWNER_OR_EXISTS_MSG)
        else:
            record = '{' + str(record['id']) + '}' + record['name'] + ','
            config.write('record_wan', record)
            click.echo(REC_WRITE_SUCCESS.format('WAN'))

    return


@cli.command(help=TWO_HELP_MSG)
@click.option('-f', '--force', default=False, flag_value=True,
              help='Force the update of your records.')
@click.option('-s', '--silent', default=False, flag_value=True,
              help='Do not display any output.')
def two(force, silent):
    if not config.token:
        raise EnlightnsException(AUTHENTICATE_MSG)

    if not (config.token and config.record_lan and config.record_wan):
        raise EnlightnsException(TWO_WAY_CFG_MSG)
    else:
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

        if not result and not silent:
            click.echo('No update needed for the LAN Record')

        # identify the WAN IP address by resolving the record
        pk, record = config.get_record_and_pk(config.record_wan)
        record_ip = resolve_a_record(record)
        record_ip = list(set(record_ip))
        if wan_ip not in record_ip or len(record_ip) > 1 or force:
            result = api.update(pk, wan_ip)

        if result and not silent:
            click.echo(result['name'] + '\t' + result['content'])

        if not result and not silent:
            click.echo('No update needed for the WAN Record')

    return


@cli.command()
@click.option('-f', '--force', default=False, flag_value=True,
              help='Force the update of your IP.')
@click.option('-s', '--silent', default=False, flag_value=True,
              help='Do not display any output.')
def update(force, silent):
    """Update your DNS record(s)"""
    if not config.token:
        raise EnlightnsException(AUTHENTICATE_MSG)

    # update only if a record is configured and that the client is authenticated
    if not (config.records and config.token and config.interface
            and config.which_ip):
        raise EnlightnsException(NOTHING_HAPPENED_MSG)

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

    return


@cli.command()
@click.option('-j', '--json', default=False, flag_value=True,
              help='Returns the IP in a JSON format.')
def wan(json):
    """Returns your public IP"""
    if not config.token:
        raise EnlightnsException(AUTHENTICATE_MSG)

    my_ip = api.ip()

    if not(json and 'ip' in my_ip):
        my_ip = my_ip['ip']

    click.echo(my_ip)

    return
