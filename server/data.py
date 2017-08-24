# -*- coding: utf-8 -*-
import threading

ST_CONNECT = 1
ST_ONLINE = 2
ST_OFFLINE = 3

global sendMsgLock
global recvMsgLock
global conn_sock
global mpOnlineUser
global mpSockBaseinfo

socketLock = threading.Lock()
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
mpSockBaseinfo = {
    sock: {
        "addr": addr,
        "user": usernum,
        "st": ST_CONNECT | ST_ONLINE | ST_OFFLINE,
    }
}
'''
mpSockBaseinfo = {}

'''
mpSockSendmsg = {
    sock: [xxx, xxx, xxx, ...],
}
'''
mpSockSendmsg = {}

'''
mpSockRecvmsg = {
    sock: [xxx, xxx, xxx, ...],
}
'''
mpSockRecvmsg = {}

#-----------------------------------------------
#when accept a new socket, we add a struct
#-----------------------------------------------
def new_connect_socket(sock, addr):
    socketLock.acquire()
    if mpSockBaseinfo.getdefault(sock, {}):
        print "repetitive new connect socket: ", sock, addr
    else:
        mpSockBaseinfo[sock] = {
            "addr": addr,
            "user": 0,
            "st": ST_CONNECT,
        }
    socketLock.release()
    return

def del_connect_socket(sock):
    socketLock.acquire()
    mpSockBaseinfo.pop(sock)
    sock.close()
    socketLock.release()
    return

def push_msg_from_recv(sock, sdata):
    recvMsgLock.acquire()
    if mpSockRecvmsg.getdefault(sock, None):
        mpSockRecvmsg[sock].append(sdata)
    recvMsgLock.release()
    return

def pop_msg_from_recv(sock):
    recvMsgLock.acquire()
    sdata = ''
    if mpSockRecvmsg.getdefault(sock, None):
        if len(mpSockRecvmsg[sock]) > 0:
            sdata = mpSockRecvmsg[sock][0]
            mpSockRecvmsg[sock] = mpSockRecvmsg[sock][1:]
    recvMsgLock.release()
    return sdata

def has_msg_from_recv(sock):
    recvMsgLock.acquire()
    has = 0
    if mpSockRecvmsg.getdefault(sock, None):
        if len(mpSockRecvmsg[sock]) > 0:
            has = 1
    recvMsgLock.release()
    return has

def push_msg_to_send(sock, sdata):
    sendMsgLock.acquire()
    if mpSockSendmsg.getdefault(sock, None):
        mpSockSendmsg[sock].append(sdata)
    sendMsgLock.release()
    return

def pop_msg_to_send(sock):
    sendMsgLock.acquire()
    sdata = ''
    if mpSockSendmsg.getdefault(sock, None):
        if len(mpSockSendmsg[sock]) > 0:
            sdata = mpSockSendmsg[sock][0]
            mpSockSendmsg[sock] = mpSockSendmsg[sock][1:]
    sendMsgLock.release()
    return sdata

def has_msg_to_send(sock):
    sendMsgLock.acquire()
    has = 0
    if mpSockSendmsg.getdefault(sock, None):
        if len(mpSockSendmsg[sock]) > 0:
            has = 1
    sendMsgLock.release()
    return has
