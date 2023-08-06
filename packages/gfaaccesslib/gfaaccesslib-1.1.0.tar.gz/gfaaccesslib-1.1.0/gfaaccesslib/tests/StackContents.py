#!/usr/bin/env python2.7
from gfaaccesslib.gfa import GFA
from gfaaccesslib.api_helpers import GFAExposureStack, GFAStandardExposureBuilder, GFACCDGeom, GFAExposeMode
from gfaaccesslib.logger import log, formatter
import logging

# create console handler to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)


IP_HOME = '127.0.0.1'
IP_EMBED = '172.16.17.140'

IP = IP_EMBED
PORT = 32000

log.info('Configured GFA to ip {0} - port {1}'.format(IP, PORT))
gfa = GFA(IP, PORT)

g = gfa.clockmanager.stack
g.add_new_image_cmd(100015050)
g.add_set_modes_cmd(True, False, True, False)
g.add_set_modes_cmd(False, True, False, True)
for _ in range(20):
    g.add_dump_rows_cmd(2048)
g.add_wait_cmd(20*60*1000)
g.add_accumulate_rows_cmd(200)
g.add_read_rows_cmd(2000)
g.add_none_cmd()
log.info('Exposure stack contents: {0}'.format(g))

ans = gfa.clockmanager.remote_set_stack_contents()
log.info("Set Stack contents Answer: {0}".format(ans))

ans = gfa.clockmanager.remote_get_stack_contents()

log.info("Contents: {0}".format(g))
log.info("Answer: {0}".format(ans))

stack = GFAStandardExposureBuilder(gfa.clockmanager.geom_conf, 1503)
stack.integration_time = 66
stack.mode = GFAExposeMode.roi
for i in range(10):
    stack.rois.add_roi_geom(row_init=i*100, col_init=120+i*10, width=50, height=50)
gfa.clockmanager.remote_set_stack_contents(stack.build())

ans = gfa.clockmanager.remote_get_stack_contents()

log.info("Contents: {0}".format(g))
log.info("Answer: {0}".format(ans))
