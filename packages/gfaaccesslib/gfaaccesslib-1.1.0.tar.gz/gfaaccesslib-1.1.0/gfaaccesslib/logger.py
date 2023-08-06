import logging
import logging.handlers

log = logging.getLogger('gfalib')
log.setLevel(logging.DEBUG)

nh = logging.NullHandler()
log.addHandler(nh)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def add_file_handler(file_path='/var/log/gfalib.log', level=logging.DEBUG):
    global log
    global formatter
    fh = logging.FileHandler(filename=file_path)
    fh.setLevel(level=level)
    # create formatter and add it to the handlers
    fh.setFormatter(formatter)
    log.addHandler(fh)
