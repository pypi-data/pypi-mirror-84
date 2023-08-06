#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from gfaaccesslib.gfa import GFA
from gfaaccesslib.logger import log, formatter
from gfaaccesslib.comm.communication import resources_callback_log, async_img_done_callback_log, async_img_start_callback_log
import logging
import time
import numpy as np

__author__ = 'otger'

# create console handler to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)

IP_DESKTOP = '172.16.17.27'
IP_EMBEDDED = '172.16.17.140'
IP_HOME = '192.168.0.167'

IP = '172.16.12.251'
PORT = 32000
APORT = 32001


def power_up():
    gfa = GFA(IP, PORT)
    print(gfa.exposecontroller.status)
    gfa.exposecontroller.remote_power_up()
    gfa.exposecontroller.remote_get_status()
    print(gfa.exposecontroller.status)


def multi_image_show():
    gfa = GFA(IP, PORT, APORT)
    gfa.async.add_resources_callback(resources_callback_log)

    for mode in range(7):
        gfa.buffers.remote_set_data_provider(0, mode)

        gfa.clockmanager.remote_clear_stack_execution_pointer()
        gfa.exposecontroller.remote_get_status()
        print(gfa.exposecontroller.status)
        gfa.exposecontroller.remote_start_stack_exec()

        time.sleep(3)
        im = gfa.raws.get_image(sorted(gfa.raws.list_images())[-1])
        im.show_im()

    log.info("Closing")
    gfa.close()
    log.info("Closed")


def check_image_5(im):

    size = im.amplifiers[0].rows[0].data.size
    comparer = np.array(list(range(1, size+1)))
    for amp in im.amplifiers:
        for row in amp.rows:
            if np.array_equal(comparer, row.data) is False:
                print(row.data)
                return False

    return True


def until_fail():
    gfa = GFA(IP, PORT, APORT)
    gfa.async.add_resources_callback(resources_callback_log)
    gfa.buffers.remote_set_data_provider(1, 5)

    while True:
        gfa.clockmanager.remote_clear_stack_execution_pointer()
        gfa.exposecontroller.remote_start_stack_exec()

        time.sleep(3)
        last_im = sorted(gfa.raws.list_images())[-1]
        if not check_image_5(gfa.raws.get_image(last_im)):
            break
        gfa.raws.rem_image(last_im)

    log.info("Closing")
    gfa.close()
    log.info("Closed")


def take_image():
    gfa = GFA(IP, PORT, APORT)
    gfa.buffers.remote_set_data_provider(0, 3)
    gfa.async.add_resources_callback(resources_callback_log)

    gfa.clockmanager.remote_clear_stack_execution_pointer()
    gfa.exposecontroller.remote_get_status()
    print(gfa.exposecontroller.status)
    gfa.exposecontroller.remote_start_stack_exec()


    # for i in range(10):
    #     time.sleep(1)
        # gfa.exposecontroller.get_status()
        # print gfa.exposecontroller.status
    # time.sleep(5)
    # for i in range(5):
    #     time.sleep(1)
    #     gfa.exposecontroller.get_status()
    #     print gfa.exposecontroller.status

    time.sleep(4)
    im = gfa.raws.get_image(sorted(gfa.raws.list_images())[-1])
    im.show_im()

    log.info("Closing")
    gfa.close()
    log.info("Closed")

def main():
    log.info('Configured GFA to ip {0} - port {1}'.format(IP, PORT))

    # power_up()
    #take_image()
    # multi_image_show()
    until_fail()

if __name__ == "__main__":
    main()

