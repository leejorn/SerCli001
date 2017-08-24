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

def process_socket():
    global lsConnSock, lsReadSock, lsWriteSock, lsErrorSock
    lsConnSock = []
    mpSockCmd = {}

    conn_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock1.setblocking(0) 
    conn_sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn_sock1.bind(('', 10011))
    conn_sock1.listen(5)

    lsConnSock.append(conn_sock1)

    print "bind sock is : ", conn_sock1

    while True:
        lsReadSock = []
        lsWriteSock = []
        lsErrorSock = []

        lsReadSock.append(conn_sock1)
        lsErrorSock.append(conn_sock1)

        for sock, mpinfo in mpSockCmd.iteritems():
            if len(mpinfo["send_cmds"]) > 0:
                lsWriteSock.append(sock)
            lsReadSock.append(sock)
            lsErrorSock.append(sock)

        rlist, wlist, xlist = select.select(lsReadSock, lsWriteSock, lsErrorSock, 0.1)

        for sock in rlist:
            if sock in lsConnSock:
                conn, addr = sock.accept()
                conn.setblocking(0)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                mpSockCmd.setdefault(conn, {"send_cmds" : ["Welcome to this ChatRoom!!\n",], "addr": addr})
                print "accept connect socket[%s] addr[%s] "%(conn, addr)
            else:
                try:
                    sdata = sock.recv(1024)
                except socket.error as e:
                    print "Error recv data. [%s]"%e
                    continue

                if len(sdata) == 0:
                    continue
                    
                mpSockCmd[sock]["send_cmds"].append(sdata)
                print "recv socket[%s] msg[%s] "%(sock, sdata)

        for sock in wlist:
            if len(mpSockCmd[sock]["send_cmds"]) == 0:
                continue

            msg = mpSockCmd[sock]["send_cmds"][0]
            mpSockCmd[sock]["send_cmds"] = mpSockCmd[sock]["send_cmds"][1:]
            try:
                sock.send("[%s] we recv your words [%s]\n"%(time.strftime("%Y-%m-%d %H:%M:%S"), msg))
                print "send socket[%s] msg[%s]"%(sock, msg)
            except socket.error as e:
                print "Error send data. [%s]"%e
                sock.close()
                mpSockCmd.pop(sock)

    conn_sock1.close()
    return

def process_rpc():
    pass

def process_db():
    pass

def main():

    socket_threading = threading.Thread(target = process_socket, args = ([]))
    rpc_threading = threading.Thread(target = process_rpc, args = ([]))
    db_threading = threading.Thread(target = process_db, args = ([]))

    socket_threading.start()
    rpc_threading.start()
    db_threading.start()

    socket_threading.join()
    rpc_threading.join()
    db_threading.join()

    sys.exit(-1)

if __name__ == "__main__":
    main()
