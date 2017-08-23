# -*- coding: utf-8 -*-

import socket
from data import *

def process_send():
    while True:
        sleep(0.1)

        lsWriteSock = []
        lsErrorSock = []

        for sock, mpInfo in mpAllSock.iteritems():
            if mpInfo["st"] = ST_OFFLINE:
                continue

            if mpInfo["sendmsg"] = '':
                continue

            sock = mpInfo["sock"]
            lsWriteSock.append(sock)
            lsErrorSock.append(sock)

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
