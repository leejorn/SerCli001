# -*- coding: utf-8 -*-
import threading

global sendMsgLock
global recvMsgLock
global lsSendMsg
global lsRecvMsg

sendMsgLock = threading.Lock()
recvMsgLock = threading.Lock()

lsSendMsg = [] 
lsRecvMsg = []

def push_msg_to_send(msg):
    global sendMsgLock, lsSendMsg
    sendMsgLock.acquire()
    lsSendMsg.append(msg)
    sendMsgLock.release()

def pop_msg_to_send():
    global sendMsgLock, lsSendMsg
    sendMsgLock.acquire()
    if len(lsSendMsg) == 0:
        msg = ''
    else:
        msg = lsSendMsg[0]
        lsSendMsg = lsSendMsg[1:]
    sendMsgLock.release()
    return msg

def push_msg_from_recv(msg):
    global recvMsgLock, lsRecvMsg
    recvMsgLock.acquire()
    lsRecvMsg.append(msg)
    recvMsgLock.release()

def pop_msg_from_recv():
    global recvMsgLock, lsRecvMsg
    recvMsgLock.acquire()
    if len(lsRecvMsg) == 0:
        msg = ''
    else:
        msg = lsRecvMsg[0]
        lsRecvMsg = lsRecvMsg[1:]
    recvMsgLock.release()
    return msg
