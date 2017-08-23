# -*- coding: utf-8 -*-

import socket
from data import *

def process_recv():
    conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock.setblocking(0)
    conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn_sock.bind(("", 10011))
    conn_sock.listen(5)

    while True:
        lsReadSock = []
        lsErrorSock = []

        lsReadSock.append(conn_sock)

        for usernum, mpInfo in mpOnlineUser.iteritems():
            if mpInfo["st"] == ST_OFFLINE:
                continue

            sock = mpInfo["sock"]
            lsReadSock.append(sock)
            lsErrorSock.append(sock)

        rlist, wlist, xlist = select.select(lsReadSock, [], lsErrorSock, 0)

        for sock in rlist:
            if sock == conn_sock:
                newsock, addr = sock.accept()
                new_connect_socket(newsock, addr)
            else:
                sdata = ""
                while True:
                    try:
                        srecv = sock.recv(1024)
                    except socket.error as e:
                        print "sock[%s] recv msg error: ", sock, e
                        continue
                    if len(srecv) == 0:
                        break
                    sdata += srecv
                push_msg_from_recv(sock, sdata)

        for sock in xlist:
            pass
