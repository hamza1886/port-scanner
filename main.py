import socket
import threading
from queue import Queue


def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except OSError:
        return False


def fill_queue(ports):
    for port in ports:
        queue.put(port)


def worker():
    while not queue.empty():
        port = queue.get()
        if scan_port(port):
            print('Port {} is open.'.format(port))
            open_ports.append(port)


if __name__ == '__main__':
    # replace it with real IP address
    target = '127.0.0.1'

    # From 0 to 1023 – well known ports assigned to common protocols and services
    # From 1024 to 49151 – registered ports assigned by ICANN to a specific service
    # From 49152 to 65535 – dynamic (private, high) ports range from 49,152 to 65,535.
    #   Can be used by any service on an ad hoc basis. Ports are assigned when a session
    #   is established, and released when the session ends.
    # See: https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
    # See: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
    ports_to_scan = range(0, 1024)

    threads = []
    open_ports = []
    queue = Queue()

    # queue ports to scan
    fill_queue(ports_to_scan)

    # create threads
    for _ in range(500):
        thread = threading.Thread(target=worker)
        threads.append(thread)

    # start threads
    for thread in threads:
        thread.start()

    # join threads (to wait for all thread to finish)
    for thread in threads:
        thread.join()

    print('Open ports are:', open_ports)
