#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'otger'

from gfaaccesslib.gfa import GFA
from gfaaccesslib.logger import log, formatter
from gfaaccesslib.comm.communication import resources_callback_log
import logging
import time

__author__ = 'otger'

# create console handler to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)

IP_DESKTOP = '172.16.17.27'
IP_EMBEDDED = '172.16.17.140'
IP_HOME = '192.168.0.167'

IP = IP_EMBEDDED
PORT = 32000
APORT = 32001

gfa = GFA(IP, PORT, APORT)

ans = gfa.buffers.remote_get_data_mode()
print("get fake data mode: {0}".format(ans))
print("status: ", gfa.buffers.status)

for i in range(20):

    gfa.clockmanager.remote_clear_stack_execution_pointer()
    gfa.clockmanager.remote_get_status()
    gfa.exposecontroller.remote_start_stack_exec()
    print(i)
    time.sleep(6)

print(gfa.raws._images)
gfa.close()