#*_* coding=utf8 *_*
#!/usr/bin/env python

import os
import signal

def drop_terminal():
    """ 让程序(Gui程序)脱离terminal运行。 """
    # drop tty
    if os.fork() != 0:
        os._exit(0)  # pylint: disable=W0212

    os.setsid()

    # drop stdio
    for fd in range(0, 2):
        try:
            os.close(fd)
        except OSError:
            pass

    os.open(os.devnull, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)

    signal.signal(signal.SIGHUP, signal.SIG_IGN)