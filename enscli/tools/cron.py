# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import getpass
import platform

from crontab import CronTab

# Setup the configuration filename for Windows
filename = 'filename.tab' if any(platform.win32_ver()) else False


def create_a_cron(ttl, action, comment):
    """This function creates a cron in the system file.

    :param ttl: the time to update the cron
    :param time: the command line action to execute
    :param comment: the comment about the job

    :returns: the newly created cron"""

    if filename:
        cron = CronTab(user=getpass.getuser(), tabfile=filename)
    else:
        cron = CronTab(user=getpass.getuser())

    custom_cmd = ' enlightns-cli ' + action

    job = cron.new(command=custom_cmd, comment=comment)
    job.minute.every(ttl / 60)
    job.enable()
    cron.write()

    return job.is_valid()

