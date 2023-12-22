#! /usr/bin/python

import signal



def handle_ctrl_c(signal, frame):
        sys.exit(130)
#This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)
    