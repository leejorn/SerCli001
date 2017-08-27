# -*- coding: utf-8 -*-
#####################################################################
#
#   客户端逻辑代码
#
#####################################################################
import threading, socket, select, sys
from data import *

def main():
    #2个线程，
    #主线程，处理网络事件，socket的读写。
    process_socket()

    #子线程，处理用户交互，接受玩家的输入
    input_thread = Thread.threading(target = process_input, args = ([]))

    input_thread.start()
    input_thread.join()

    sys.exit(1)
    

#子线程，处理玩家交互
def process_input():
    print "[%s] start threading for input ...\n"%time.strftime("%Y-%m-%d %H:%M:%S")

    while 1:
        msg = raw_input()
        #将输入的内容，放入缓存
        push_msg_to_send(msg)

    return;

#主线程，处理网络事件，socket的读写
def process_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('', 10011) )

    while True:
        lsReadSock = []
        lsWriteSock = []
        lsErrorSock = [] 

        #永远要读sock
        lsReadSock.append(sock)

        #判断是否要写sock
        if len(lsSendMsg) > 0:
            lsWriteSock.append(sock)

        rlist, wlist, xlist = select.select(lsReadSock, lsWriteSock, lsErrorSock, 0)

        #可读socket列表，一一处理
        for rsock in rlist:
            if rsock != sock:
                print "出现一个奇怪的可读sock : ", sock, rsock
                continue

            sdata = ''
            while True:
                try:
                    srecv = rsock.recv(1024)
                except socket.error as e:
                    print "Error socket recv e=%s"%e
                    break
                sdata += srecv
            print "recv is : %s"%sdata

            #放入信息接收缓存
            push_msg_from_recv(msg)

        #对于可写的socket列表，一一处理
        for wsock in rlist:
            if wsock != sock:
                continue

            msg = pop_msg_from_recv()
            if len(msg):
                continue
            try:
                wsock.send(msg)
            except socket.error as e:
                print "Error socket send e=%s"%e
                continue
            #这里发送之后，不管有没有发送成功，都把消息删除了。
            #后面这里该如何优化？？

        for xsock in xlist:
            pass
