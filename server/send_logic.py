# -*- coding: utf-8 -*-

import socket
from data import *

def process_send():
    while True:
        sleep(0.1)

        lsWriteSock = []
        lsErrorSock = []

        for usernum, mpInfo in mpOnlineUser.iteritems():
            if mpInfo["st"] = ST_WAIT_OFFLINE:
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
            pass
