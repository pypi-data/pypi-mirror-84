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

gfa = GFA(IP, PORT)

ans = gfa.buffers.remote_get_data_mode()
print("get fake data mode: {0}".format(ans))
print("status: ", gfa.buffers.status)

ans = gfa.buffers.remote_get_buffers_status()
print("get buffers status: {0}".format(ans))
print("status: ", gfa.buffers.status)

gfa.close()