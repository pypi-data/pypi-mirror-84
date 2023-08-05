import socket
import fire
import sys
import logging
import errno
import time

socket_singleton = None


def ensure_singleton(port, log_error=True):
    """After calling this method, you can be assured no other script will be running with this port.
    Otherwise, script will exit with warning
    """
    # from here:
    # https://stackoverflow.com/questions/380870/make-sure-only-a-single-instance-of-a-program-is-running
    global socket_singleton
    if socket_singleton is not None:
        raise Exception('You already called this method')
    if port_is_locked(port):
        if log_error:
            logging.error('port: %i is already locked so exiting' % port)
        sys.exit(1)
    socket_singleton = lock_port(port)
    if socket_singleton is None:
        if log_error:
            logging.error('Error getting lock on port: %i, so exiting' % port)
        sys.exit(1)


def lock_port(port, retries=0, sleep_for=1.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in range(retries + 1):
        try:
            s.bind(("127.0.0.1", port))
            return s
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                pass
        if retries > 0:
            time.sleep(sleep_for)
    return None


def port_is_locked(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", port))
        s.close()
        return False
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            return True


def busy_ports(start, end):
    busy = 0
    for port in range(start, end + 1):
        if port_is_locked(port):
            busy += 1
    return busy


def first_open_port(start, end):
    # start and end are inclusive
    for port in range(start, end + 1):
        e = lock_port(port, retries=0)
        if e is not None:
            return e, port
    return None, None


if __name__ == '__main__':
    fire.Fire()
