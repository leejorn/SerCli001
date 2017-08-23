# -*- coding: utf-8 -*-
import threading

ST_CONNECT = 1
ST_ONLINE = 2
ST_OFFLINE = 3

global sendMsgLock
global recvMsgLock
global conn_sock
global mpOnlineUser
global mpAllSock

sendMsgLock = threading.Lock()
recvMsgLock = threading.Lock()

conn_sock = None

'''
mpOnlineUser = {
    usernum: {
        "sock": sock,
        ...
    }
}
'''
mpOnlineUser = {}

'''
mpAllSock = {
    sock: {
        "addr": addr,
        "user": usernum,
        "st": ST_ONLINE | ST_OFFLINE,
        "sendmsg": [xxx, xxx, xxx, ...],
        "recvmsg": [xxx, xxx, xxx, ...],
    }
}
'''
mpAllSock = {}

#-----------------------------------------------
#when accept a new socket, we add a struct
#-----------------------------------------------
def new_connect_socket(sock, addr):
    if mpAllSock.getdefault(sock, {}):
        print "repetitive new connect socket: ", sock, addr
        return

    mpAllSock[sock] = {
        "addr": addr,
        "user": 0,
        "st": ST_CONNECT,
        "sendmsg": [],
        "recvmsg": [],
    }
    return

def push_msg_from_recv(sock, sdata):
    recvMsgLock.acquire()
    if not mpAllSock.getdefault(sock, None):
        print "Error no data, sock=", sock
    else:
        mpAllSock[sock]["recvmsg"].append(sdata)
    recvMsgLock.release()
    return

def pop_msg_from_recv(sock):
    recvMsgLock.acquire()
    sdata = ''
    if not mpAllSock.getdefault(sock, None):
        print "Error no data, sock=", sock
    else:
        if len(mpAllSock[sock]["recvmsg"]) > 0:
            sdata = mpAllSock[sock]["recvmsg"][0]
            mpAllSock[sock]["recvmsg"] = mpAllSock[sock]["recvmsg"][1:]
    recvMsgLock.release()
    return sdata

def push_msg_to_send(sock, sdata):
    sendMsgLock.acquire()
    if not mpAllSock.getdefault(sock, None):
        print "Error no data, sock=", sock
    else:
        mpAllSock[sock]["sendmsg"].append(sdata)
    sendMsgLock.release()
    return

def pop_msg_to_send(sock):
    sendMsgLock.acquire()
    sdata = ''
    if not mpAllSock.getdefault(sock, None):
        print "Error no data, sock=", sock
    else:
        if len(mpAllSock[sock]["sendmsg"]) > 0:
            sdata = mpAllSock[sock]["sendmsg"][0]
            mpAllSock[sock]["sendmsg"] = mpAllSock[sock]["sendmsg"][1:]
    sendMsgLock.release()
    return sdata
