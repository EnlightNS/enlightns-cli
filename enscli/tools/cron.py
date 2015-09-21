# -*- coding: utf-8 -*-
from __future__ import absolute_import

import platform
from distutils import spawn
from datetime import datetime, timedelta

from crontab import CronTab

# Setup the configuration filename for Windows
filename = 'filename.tab' if any(platform.win32_ver()) else False
executable = spawn.find_executable('enlightns-cli')


def create_a_cron(ttl, action, comment):
    """This function creates a cron in the system file.

    :param ttl: the time to update the cron
    :param comment: the comment about the job

    :returns: the newly created cron"""

    custom_cmd = executable + ' ' + action
    is_written = False

    cron = CronTab(tabfile=filename) if filename else CronTab(user=True)

    # deletes the cron if it already exists
    cron.remove_all(comment=comment)
    cron.write()

    cron = CronTab(tabfile=filename) if filename else CronTab(user=True)
    lines = list(set(cron.lines))
    try:
        lines.remove(u'')
    except:
        pass
    cron.lines = lines

    # sets the new cron
    job = cron.new(command=custom_cmd, comment=comment)
    days, hours, minutes, seconds = extract_time(ttl)

    if minutes:
        job.minute.every(minutes)

    if hours and not minutes:
        job.hour.every(hours)

    if days and not hours and not minutes:
        job.every(days).days()

    if job.is_valid():
        cron.write()
        is_written = True

    return is_written, job.cron.render()


def extract_time(seconds):
    """This function extracts the time of the DNS record and convert it in
    second, minute, hour and day

    e.g.:

        84600 == 0 minutes 0 hours 1 day

    :param seconds: the TTL in seconds to convert

    :return: days, hours, minutes, seconds values out of the seconds
    """
    sec = timedelta(seconds=seconds)
    my_date = datetime(1, 1, 1) + sec

    return my_date.day-1, my_date.hour, my_date.minute, my_date.second
