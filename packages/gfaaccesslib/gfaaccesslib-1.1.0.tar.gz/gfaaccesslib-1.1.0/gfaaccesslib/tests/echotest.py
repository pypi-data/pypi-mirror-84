from gfaaccesslib.gfa import GFA
import time
from gfaaccesslib.logger import log, formatter
import logging

# create console handler to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
log.addHandler(ch)

IP = "172.16.12.251"
PORT = 32000

log.info('Configured GFA to ip {0} - port {1}'.format(IP, PORT))
gfa = GFA(IP, PORT)

NUM_ELEMENTS = 200
start = time.time()
total = 0
for i in range(NUM_ELEMENTS):
    e = gfa.tests.echo('Los Libios Marty!'+'abcdefghijklmnopqrstuvwxyz0123456789,.abc+*/-defgh'*90)
    total += e.elapsed_ms
log.info("{0} accesses - average: {1} ms".format(NUM_ELEMENTS, 1.0*total/NUM_ELEMENTS))
log.info("Total time: {0}".format(time.time()-start))


log.info("Waiting for 3 seconds")
e = gfa.tests.wait(3000)

log.info("Waiting for 3 seconds in a thread")
e = gfa.tests.long_threaded_command(3000)

try:
    gfa.tests.bravo()

except Exception as e:
    log.info("An exception happened")
    log.info(e)
else:
    raise Exception("An exception of an unimplemented command should have been risen")

log.info('Sent bytes: {0}'.format(gfa.comm.stats.sent_bytes_stats))
log.info('Received bytes: {0}'.format(gfa.comm.stats.rcvd_bytes_stats))
