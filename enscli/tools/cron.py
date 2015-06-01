# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import platform
from distutils import spawn

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

    # sets the new cron
    job = cron.new(command=custom_cmd, comment=comment)
    job.minute.every(ttl / 60)

    if job.is_valid():
        cron.write()
        is_written = True

    return is_written, job.cron.render()

