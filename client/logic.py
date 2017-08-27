# -*- coding: utf-8 -*-
#####################################################################
#
#
#####################################################################
import threading, socket, select, sys, time
from data import *

def main():
    socket_thread = threading.Thread(target = process_socket, args = ([]))
    input_thread = threading.Thread(target = process_input, args = ([]))

    socket_thread.start()
    input_thread.start()

    socket_thread.join()
    input_thread.join()

    sys.exit(1)
    
def process_input():
    print "[%s] start threading for input ...\n"%time.strftime("%Y-%m-%d %H:%M:%S")

    while 1:
        msg = raw_input()
        push_msg_to_send(msg)

    return;

def process_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('', 10011) )

    while True:
        lsReadSock = []
        lsWriteSock = []
        lsErrorSock = [] 

        lsReadSock.append(sock)
        
        #whatever we need to write the sock, we shelled append the sock to lsWriteSock
        lsWriteSock.append(sock)

        rlist, wlist, xlist = select.select(lsReadSock, lsWriteSock, lsErrorSock, 0)

        for rsock in rlist:
            if rsock != sock:
                print "there is a unknown sock be readed: ", sock, rsock
                continue

            sdata = ''
            while True:
                try:
                    srecv = rsock.recv(1024)
                except socket.error as e:
                    print "Error socket recv e=%s"%e
                    break
                if len(srecv) == 0:
                    break
                sdata += srecv
            print "recv is : %s"%sdata

            push_msg_from_recv(msg)

        for wsock in wlist:
            if wsock != sock:
                continue

            msg = pop_msg_to_send()
            if len(msg):
                continue
            try:
                wsock.send(msg)
            except socket.error as e:
                print "Error socket send e=%s"%e
                continue

        for xsock in xlist:
            pass
