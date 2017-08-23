# -*- coding: utf-8 -*-
import time, threading, socket, select, sys

global lsConnSock
global lsReadSock
global lsWriteSock
global lsErrorSock

mpSockCmd = {}
cmdLock = threading.Lock()

def init_sock_cmd(sock):
    cmdLock.acquire()
    mpSockCmd.setdefault(sock, {})
    mpSockCmd[sock] = {
            "recv_buff" : "",
            "recv_cmds" : [],

            "send_cmds" : [], 
            "send_buff" : "", 
            }
    cmdLock.release()

def add_sock_cmd(sock, cmd, args):
    cmdLock.acquire()
    mpSockCmd[sock]["send_cmds"].append((cmd, args))
    cmdLock.release()

def process_send():
    pass

def process_recv():
    global lsConnSock, lsReadSock, lsWriteSock, lsErrorSock
    lsConnSock = []
    lsReadSock = []
    lsWriteSock = []
    lsErrorSock = []
    mpSockCmd = {}

    conn_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock1.setblocking(0) 
    conn_sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn_sock1.bind(('', 10011))
    conn_sock1.listen(5)

    lsConnSock.append(conn_sock1)

    lsReadSock.append(conn_sock1)

    print "bind sock is : ", conn_sock1

    while 1:
        rlist, wlist, xlist = select.select(lsReadSock, lsWriteSock, lsErrorSock, 0)

        if rlist:
            print "rlist select : ", rlist, wlist, xlist

        if wlist:
            print "wlist select : ", rlist, wlist, xlist

        for sock in rlist:
            if sock in lsConnSock:
                conn, addr = sock.accept()
                conn.setblocking(0)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                mpSockCmd.setdefault(conn, {"msg" : ["Welcome to this ChatRoom!!\n",], "addr": addr})
                lsReadSock.append(conn)
                lsWriteSock.append(conn)
                print "accept sock is : ", conn
            else:
                try:
                    sdata = sock.recv(1024)
                except socket.error as e:
                    print "Error recv data. [%s]"%e
                    continue
                    
                mpSockCmd[sock]["msg"].append(sdata)
                print "receive sdata = ", sdata

                if sock not in lsWriteSock:
                    lsWriteSock.append(sock)

        for sock in wlist:
            while len(mpSockCmd[sock]["msg"]) > 0:
                msg = mpSockCmd[sock]["msg"][0]
                mpSockCmd[sock]["msg"] = mpSockCmd[sock]["msg"][1:]
                print "send msg : %s\n"%msg
                try:
                    sock.send("[%s] we recv your words [%s]\n"%(time.strftime("%Y-%m-%d %H:%M:%S"), msg))
                except socket.error as e:
                    print "Error send data. [%s]"%e
                    sock.close()
                    if sock in lsReadSock:
                        lsReadSock.remove(sock)
            lsWriteSock.remove(sock)

    conn_sock1.close()

def process_rpc():
    pass

def process_db():
    pass

def main():

    recv_threading = threading.Thread(target = process_recv, args = ([]))
    send_threading = threading.Thread(target = process_send, args = ([]))
    rpc_threading = threading.Thread(target = process_rpc, args = ([]))
    db_threading = threading.Thread(target = process_db, args = ([]))

    recv_threading.start()
    send_threading.start()
    rpc_threading.start()
    db_threading.start()

    recv_threading.join()
    send_threading.join()
    rpc_threading.join()
    db_threading.join()

    sys.exit(-1)

if __name__ == "__main__":
    main()
