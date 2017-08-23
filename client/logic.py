# -*- coding: utf-8 -*-
#####################################################################
#
#
#####################################################################
import threading, socket, select, sys, time
from data import *

global sock

def main():
    recv_thread = threading.Thread(target = process_recv, args = ([]))
    send_thread = threading.Thread(target = process_send, args = ([]))
    input_thread = threading.Thread(target = process_input, args = ([]))

    recv_thread.start()
    send_thread.start()
    input_thread.start()

    recv_thread.join()
    send_thread.join()
    input_thread.join()

    sys.exit(1)
    
def process_input():
    print "[%s] start threading for input ...\n"%time.strftime("%Y-%m-%d %H:%M:%S")

    while 1:
        msg = raw_input()
        push_msg_to_send(msg)

    return

def process_send():
    while True:
        time.sleep(0.2)

        if not sock:
            continue

        msg = pop_msg_to_send()
        if len(msg) == 0:
            continue

        lsWriteSock = [ sock, ]
        lsErrorSock = [ sock, ] 
        rlist, wlist, xlist = select.select([], lsWriteSock, lsErrorSock, 0)

        for wsock in wlist:
            if wsock != sock:
                print "there is a unknown sock be writed: ", sock, wsock
                continue

            try:
                wsock.send(msg)
            except socket.error as e:
                print "Error socket send e=%s"%e
                continue

    return

def process_recv():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('', 10011) )

    while True:
        lsReadSock = [ sock, ]
        lsErrorSock = [ sock, ] 

        rlist, wlist, xlist = select.select(lsReadSock, [], lsErrorSock, 0)

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

            if len(sdata) == 0:
                continue
            push_msg_from_recv(msg)
            print "recv from remote msg is : ", msg

        for xsock in xlist:
            pass
