#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from gfaaccesslib.gfa import GFA
from gfaaccesslib.logger import log, formatter
import logging

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

def power_up(gfa=None):
    if gfa is None:
        gfa = GFA(IP, PORT)
    print(gfa.exposecontroller.status)
    gfa.exposecontroller.remote_power_up()
    gfa.exposecontroller.remote_get_status()
    print(gfa.exposecontroller.status)

def main():
    log.info('Configured GFA to ip {0} - port {1}'.format(IP, PORT))
    gfa = GFA(IP, PORT)

    print(gfa.powercontroller.enables)
    print(gfa.powercontroller.voltages)

    gfa.powercontroller.voltages.RG_hi.volts = 10
    gfa.powercontroller.remote_set_voltages()
    print(gfa.powercontroller.voltages)

    print("power up timing: {0}".format(gfa.powercontroller.powerup_timing_ms))
    print("power down timing: {0}".format(gfa.powercontroller.powerdown_timing_ms))

    gfa.powercontroller.remote_get_phase_timing()
    print("power up timing: {0}".format(gfa.powercontroller.powerup_timing_ms))
    print("power down timing: {0}".format(gfa.powercontroller.powerdown_timing_ms))

    gfa.powercontroller.powerup_timing_ms = 155
    gfa.powercontroller.powerdown_timing_ms = 666

    gfa.powercontroller.remote_set_phase_timing()
    print("power up timing: {0}".format(gfa.powercontroller.powerup_timing_ms))
    print("power down timing: {0}".format(gfa.powercontroller.powerdown_timing_ms))

    gfa.powercontroller.remote_get_phase_timing()
    print("power up timing: {0}".format(gfa.powercontroller.powerup_timing_ms))
    print("power down timing: {0}".format(gfa.powercontroller.powerdown_timing_ms))

    power_up(gfa)

if __name__ == "__main__":
    main()

