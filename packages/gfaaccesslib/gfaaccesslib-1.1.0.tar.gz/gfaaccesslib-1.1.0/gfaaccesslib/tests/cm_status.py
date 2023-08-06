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

IP = IP_HOME
PORT = 32000


def main():
    log.info('Configured GFA to ip {0} - port {1}'.format(IP, PORT))
    gfa = GFA(IP, PORT)

    ans = gfa.clockmanager.remote_get_status()
    log.info('{0}'.format(ans.json))
    log.info('Status: {0}'.format(gfa.clockmanager.status))
    if gfa.clockmanager.status.stack_empty:
        gfa.clockmanager.stack.add_new_image_cmd(1002)
    gfa.clockmanager.remote_clear_stack()
    log.info('stack should be empty: {0}'.format(gfa.clockmanager.status.stack_empty))


class TestClockManagerStatus(unittest.TestCase):

    def setUp(self):
        self.gfa = GFA(IP, PORT)

    def testClearStack(self):
        if self.gfa.clockmanager.status.stack_empty:
            self.gfa.clockmanager.stack.add_new_image_cmd(1002)
        self.assertEqual(self.gfa.clockmanager.status.stack_empty, False, "Stack should not be empty")
        self.gfa.clockmanager.remote_clear_stack()
        self.gfa.clockmanager.remote_get_status()
        self.assertEqual(self.gfa.clockmanager.status.stack_empty, True, "Stack should be empty")

if __name__ == "__main__":
    unittest.main()

    # main()