# -*- coding: utf-8 -*-

import socket
from data import *

def process_send():
    while True:
        sleep(0.1)

        lsWriteSock = []
        lsErrorSock = []

        socketLock.acquire()
        for sock, mpInfo in mpSockBaseinfo.iteritems():
            if mpInfo["st"] = ST_OFFLINE:
                continue

            if not has_msg_to_send(sock):
                continue

            sock = mpInfo["sock"]
            lsWriteSock.append(sock)
            lsErrorSock.append(sock)
        socketLock.release()

        if len(lsWriteSock) == 0:
            continue

        rlist, wlist, xlist = select.select([], lsWriteSock, lsErrorSock, 0)

        for sock in wlist:
            msg = pop_msg_to_send(sock)
            if len(msg) == 0:
                continue

            try:
                sock.send(msg)
            except socket.error as e:
                print "sock[%s] send msg error: ", e
                continue

        for sock in xlist:
            pass
