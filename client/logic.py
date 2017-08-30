# -*- coding: utf-8 -*-
#####################################################################
#
#
#####################################################################
import threading, socket, select, sys, time, errno
from data import *

global sock

def main():
    socket_thread = threading.Thread(target = process_socket, args = ([]))
    input_thread = threading.Thread(target = process_input, args = ([]))

    socket_thread.start()
    input_thread.start()

    socket_thread.join()
    input_thread.join()

    sys.exit(1)

def show_cmds_help():
    pass
    
def process_input():
    print "[%s] start threading for input ...\n"%time.strftime("%Y-%m-%d %H:%M:%S")

    while True:
        try:
            st = get_st_login()
            if st == CLIENT_ST_NO_LOGIN: #not login
                msg = raw_input("Do you have registed account??(Y/N)\n>> ")
                if msg == "N":
                    print "Please regist a account first!\n"
                    name = raw_input("Please enter you name:\n>>")
                    passwd = raw_input("Please enter you passwd:\n>>")
                    msg = "REG %s %s"%(name, passwd)
                    push_msg_to_send(msg)
                elif msg == "Y":
                    name = raw_input("Please enter you name:\n>>")
                    passwd = raw_input("Please enter you passwd:\n>>")
                    msg = "ETR %s %s"%(name, passwd)
                    push_msg_to_send(msg)
            elif st == CLIENT_ST_LOGIN: #has login
                msg = raw_input("YOU TALK[you words][help]\n>>")
                if msg == "help":
                    show_cmds_help()
                    continue
                elif len(msg) == 0 or msg == "\n":
                    continue
                push_msg_to_send(msg)
        except EOFError:
            #when we get EOFError, we shell finish this program
            set_shutdown()
            break
    return

def process_socket():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect( ('', 10011) )

    while True:
        #check is now shutdown??
        if get_shutdown():
            sock.close()
            break

        lsReadSock = []
        lsWriteSock = []
        lsErrorSock = []

        lsReadSock.append(sock)
        lsErrorSock.append(sock)

        if has_msg_to_send():
            lsWriteSock.append(sock)

        rlist, wlist, xlist = select.select(lsReadSock, lsWriteSock, lsErrorSock, 0.1)

        for rsock in rlist:
            if rsock != sock:
                print "there is a unknown sock be readed: ", sock, rsock
                continue

            sdata = ''
            while True:
                try:
                    srecv = rsock.recv(1024)
                except socket.error as e:
                    if e[0] == errno.EAGAIN:
                        break
                    else:
                        print "errno = ", e[0]
                        print "Error socket recv e=%s"%e
                        break
                if len(srecv) == 0:
                    break
                sdata += srecv

            if len(sdata) == 0:
                continue
            push_msg_from_recv(sdata)
            print "recv from remote msg is : ", sdata

        for wsock in wlist:
            if wsock != sock:
                print "there is a unknown sock be writed: ", sock, wsock
                continue

            msg = pop_msg_to_send()
            if len(msg) == 0:
                continue

            try:
                wsock.send(msg)
            except socket.error as e:
                print "Error socket send e=%s"%e
                continue

        for xsock in xlist:
            pass
