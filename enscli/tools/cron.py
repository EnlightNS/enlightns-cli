# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import getpass

from crontab import CronTab


def create_a_cron(ttl, action, comment):
    """This function creates a cron in the system file.

    :param ttl: the time to update the cron
    :param time: the command line action to execute
    :param comment: the comment about the job

    :returns: the newly created cron"""

    cron = CronTab(user=getpass.getuser())

    if ttl / 60 == 1:
        time = '* * * * *'
    else:
        time = '*/{0} * * * *'.format(ttl / 60)

    custom_cmd = time + ' enlightns-cli ' + action

    job = cron.new(command=custom_cmd, comment=comment)
    if job.is_valid():
        job.enable()
        cron.write()

    return job.is_valid()

