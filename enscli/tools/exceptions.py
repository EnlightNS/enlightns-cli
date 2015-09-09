# -*- coding: utf-8 -*-
from __future__ import absolute_import

from click import ClickException, echo
from click._compat import get_text_stderr, PY2


class EnlightnsException(ClickException):
    """An exception that Click can handle and show to the user.

    We only overwrite the exception message
    """
    def __init__(self, message):
        if PY2 and message is not None:
            message = message.encode('utf-8')
        ClickException.__init__(self, message)
        self.message = message

    def show(self, file=None):
        if file is None:
            file = get_text_stderr()
        echo(self.format_message(), file=file)

