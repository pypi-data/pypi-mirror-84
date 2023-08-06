#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'otger'

from gfaaccesslib.gfa import GFA
from gfaaccesslib.api_helpers import GFAExposureStack, GFAStandardExposureBuilder, GFACCDGeom, GFAExposeMode
from gfaaccesslib.logger import log, formatter
import logging

import sys

print(sys.path)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)

IP_EMBEDDED = '172.16.17.140'
IP_HOME = '192.168.0.167'

IP = IP_EMBEDDED
PORT = 32000
APORT = 32001

log.info('Configured GFA to ip {0} - port {1}'.format(IP, PORT))

gfa = GFA(IP, PORT)

g = gfa.clockmanager.stack
g.clear()
g.add_new_image_cmd()
g.add_set_modes_cmd(True, True, True, True)
g.add_wait_cmd(1000)
g.add_dump_rows_cmd(500)
g.add_read_rows_cmd(500)
g.add_none_cmd()
log.info('Exposure stack contents: {0}'.format(g))

ans = gfa.clockmanager.remote_set_stack_contents()

log.info("Default values: {0}".format(gfa.clockmanager.time_conf))
gfa.clockmanager.remote_set_clock_timings()

geom = gfa.clockmanager.geom_conf
geom.amplifier_cols = 500
geom.overscan_cols = 0
geom.prescan_cols = 0
geom.amplifiers_fg_enable = True
geom.amplifiers_eh_enable = True

gfa.clockmanager.remote_set_ccd_geom(geom)
gfa.clockmanager.remote_get_info()
print(gfa.clockmanager.status)
print(gfa.clockmanager.info)



## Here the clockmanager is configured
