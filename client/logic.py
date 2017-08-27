# -*- coding: utf-8 -*-
#####################################################################
#
#   �ͻ����߼�����
#
#####################################################################
import threading, socket, select, sys
from data import *

def main():
    #2���̣߳�
    #���̣߳����������¼���socket�Ķ�д��
    process_socket()

    #���̣߳������û�������������ҵ�����
    input_thread = Thread.threading(target = process_input, args = ([]))

    input_thread.start()
    input_thread.join()

    sys.exit(1)
    

#���̣߳�������ҽ���
def process_input():
    print "[%s] start threading for input ...\n"%time.strftime("%Y-%m-%d %H:%M:%S")

    while 1:
        msg = raw_input()
        #����������ݣ����뻺��
        push_msg_to_send(msg)

    return;

#���̣߳����������¼���socket�Ķ�д
def process_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('', 10011) )

    while True:
        lsReadSock = []
        lsWriteSock = []
        lsErrorSock = [] 

        #��ԶҪ��sock
        lsReadSock.append(sock)

        #�ж��Ƿ�Ҫдsock
        if len(lsSendMsg) > 0:
            lsWriteSock.append(sock)

        rlist, wlist, xlist = select.select(lsReadSock, lsWriteSock, lsErrorSock, 0)

        #�ɶ�socket�б�һһ����
        for rsock in rlist:
            if rsock != sock:
                print "����һ����ֵĿɶ�sock : ", sock, rsock
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

            #������Ϣ���ջ���
            push_msg_from_recv(msg)

        #���ڿ�д��socket�б�һһ����
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
            #���﷢��֮�󣬲�����û�з��ͳɹ���������Ϣɾ���ˡ�
            #�������������Ż�����

        for xsock in xlist:
            pass
