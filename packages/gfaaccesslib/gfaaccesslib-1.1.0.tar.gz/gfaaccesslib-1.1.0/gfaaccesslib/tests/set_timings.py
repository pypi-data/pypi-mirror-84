#!/usr/bin/env python2.7
from gfaaccesslib.api_helpers import GFATimeConfiguration, GFACCDGeom
from gfaaccesslib.gfa import GFA
from gfaaccesslib.logger import log, formatter
import logging

# create console handler to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)

IP_DESKTOP = '172.16.17.27'
IP_EMBEDDED = '172.16.17.140'
IP_HOME = '127.0.0.1'

IP = IP_EMBEDDED
PORT = 32000

log.info('Configured GFA to ip {0} - port {1}'.format(IP, PORT))
gfa = GFA(IP, PORT)


log.info("Default values: {0}".format(gfa.clockmanager.time_conf))
gfa.clockmanager.remote_set_clock_timings()


ans = gfa.clockmanager.remote_get_clock_timings()
log.info("Method return value: {0}".format(ans))
log.info("Timing values: {0}".format(gfa.clockmanager.time_conf))

log.info('Default geometry values: {0}'.format(gfa.clockmanager.geom_conf))
gfa.clockmanager.remote_set_ccd_geom()

log.info('Retrieve configured geometry')
ccd_geom = gfa.clockmanager.remote_get_ccd_geom()
log.info("Type of answer: {0} - {1} - {2}".format(ccd_geom, type(ccd_geom), ccd_geom.__dict__))
log.info("CCD Geom: {0}".format(gfa.clockmanager.geom_conf))

gfa.clockmanager.geom_conf.amplifiers_eh_enable = False
gfa.clockmanager.remote_set_ccd_geom()
gfa.clockmanager.remote_get_ccd_geom()
log.info("Enabled eh: {0}".format(gfa.clockmanager.geom_conf.amplifiers_eh_enable))

gfa_ccd_geom = GFACCDGeom()
gfa_ccd_geom.set_default_values()
gfa_ccd_geom.amplifiers_fg_enable = False
gfa.clockmanager.remote_set_ccd_geom(gfa_ccd_geom)
gfa.clockmanager.remote_get_ccd_geom()
log.info("Enabled eh: {0}".format(gfa.clockmanager.geom_conf.amplifiers_eh_enable))
log.info("Enabled fg: {0}".format(gfa.clockmanager.geom_conf.amplifiers_fg_enable))
