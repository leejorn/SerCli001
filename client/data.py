# -*- coding: utf-8 -*-
import threading

sendMsgLock = threading.Lock()
recvMsgLock = threading.Lock()

lsSendMsg = [] 
lsRecvMsg = []

def push_msg_to_send(msg):
    sendMsgLock.require()
    lsSendMsg.append(msg)
    sendMsgLock.release()

def pop_msg_to_send():
    sendMsgLock.require()
    if len(lsSendMsg) == 0:
        msg = ''
    else:
        msg = lsSendMsg[0]
        lsSendMsg = lsSendMsg[1:]
    sendMsgLock.release()
    return msg

def push_msg_from_recv(msg):
    recvMsgLock.require()
    lsRecvMsg.append(msg)
    recvMsgLock.release()

def pop_msg_from_recv():
    recvMsgLock.require()
    if len(lsRecvMsg) == 0:
        msg = ''
    else:
        msg = lsRecvMsg[0]
        lsRecvMsg = lsRecvMsg[1:]
    recvMsgLock.release()
    return msg
