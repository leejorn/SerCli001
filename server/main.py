# -*- coding: utf-8 -*-
import time, threading, socket, select, sys

#socket�б�
global lsConnSock
global lsReadSock
global lsWriteSock
global lsErrorSock

mpSockCmd = {}
cmdLock = threading.Lock()

def init_sock_cmd(sock):
    cmdLock.require()
    mpSockCmd.setdefault(sock, {})
    mpSockCmd[sock] = {
            "recv_buff" : "",   #��ȡ�Ŀͻ��˵����ݣ�ȫ���ȴ�������
            "recv_cmds" : [],   #���ܵ��Ŀͻ��˵�����,�����ɵ�cmdsָ��

            "send_cmds" : [],   #��Ҫ�������ͻ��˵�ָ��ȷ�������������л�
            "send_buff" : "",   #��Ҫ���ͻ��˷��͵����ݣ�ȫ���ȴ�������
            }
    cmdLock.release()

def add_sock_cmd(sock, cmd, args):
    cmdLock.require()
    mpSockCmd[sock]["send_cmds"].append((cmd, args))
    cmdLock.release()

#����������Ǵ����������ݵ���Ҫģ��
#ʹ�÷�������socket + select��·����
def process_socket():
    global lsConnSock, lsReadSock, lsWriteSock, lsErrorSock
    lsConnSock = []
    lsReadSock = []
    lsWriteSock = []
    lsErrorSock = []
    mpSockCmd = {}

    #�����ü�����socket
    conn_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock1.setblocking(0)   #����ʹ��select��·���ã������ֱ�ӷ����� socket
    conn_sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn_sock1.bind(('', 10011))
    conn_sock1.listen(5)

    lsConnSock.append(conn_sock1)

    #��conn_sock1����ɶ��ļ���б�
    lsReadSock.append(conn_sock1)

    #����socket����OK֮�󣬿�ʼʹ��select����ظ���socket�����
    #��������ѭ��ʹ��select
    while 1:
        rlist, wlist, xlist = select.select(lsReadSock, lsWriteSock, lsErrorSock, 0)

        if rlist:
            print "select : ", rlist, wlist, xlist

        #����ɶ���socket�б�
        for sock in rlist:
            if sock in lsConnSock:
                conn, addr = sock.accept()
                conn.setblocking(0)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                mpSockCmd.setdefault(conn, {"msg" : ["Welcome to this ChatRoom!!\n",], "addr": addr})
                lsReadSock.append(conn)
                lsWriteSock.append(conn)
            else:
                try:
                    sdata = sock.recv(1024)
                except socket.error as e:
                    print "Error recv data. [%s]"%e
                    continue
                    
                mpSockCmd[sock]["msg"].append(sdata)
                print "receive sdata = ", sdata

                #������sock���ڿ�д�б��У���ô�����ȥ
                if sock not in lsWriteSock:
                    lsWriteSock.append(sock)

        #�����д��socket�б�
        for sock in wlist:
            while len(mpSockCmd[sock]["msg"]) > 0:
                msg = mpSockCmd[sock]["msg"][0]
                mpSockCmd[sock]["msg"] = mpSockCmd[sock]["msg"][1:]
                print "send msg : %s\n"%msg
                try:
                    sock.send("[%s] we recv your words [%s]\n"%(time.strftime("%Y-%m-%d %H:%M:%S"), msg))
                except socket.error as e:
                    print "Error send data. [%s]"%e
                    continue
            lsWriteSock.remove(sock) #��д���������֮��Ҫ�����ӿ�д����б���ɾ����

    conn_sock1.close()

#רע����rpcָ��������յ�����Ϣ
def process_rpc():
    pass

#רע�������ݵĴ洢
def process_db():
    pass

def main():

    #���̣߳���Ҫ����socket���ӣ���Ϣ����
    process_socket()

    #���߳�1������rpcָ��������յ�����Ϣ
    rpc_threading = threading.Thread(target = process_rpc, args = ([]))

    #���߳�2���������ݴ洢
    db_threading = threading.Thread(target = process_db, args = ([]))

    rpc_threading.start()
    db_threading.start()

    rpc_threading.join()
    db_threading.join()

    sys.exit(-1)

if __name__ == "__main__":
    main()
