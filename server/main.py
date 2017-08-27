# -*- coding: utf-8 -*-
import time, threading, socket, select, sys

#socket列表
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
            "recv_buff" : "",   #读取的客户端的内容，全部先存在这里
            "recv_cmds" : [],   #接受到的客户端的内容,解析成的cmds指令

            "send_cmds" : [],   #需要发送往客户端的指令，先放在这里，慢慢序列化
            "send_buff" : "",   #需要往客户端发送的内容，全部先存在这里
            }
    cmdLock.release()

def add_sock_cmd(sock, cmd, args):
    cmdLock.require()
    mpSockCmd[sock]["send_cmds"].append((cmd, args))
    cmdLock.release()

#这个函数就是处理网络数据的主要模块
#使用非阻塞的socket + select多路复用
def process_socket():
    global lsConnSock, lsReadSock, lsWriteSock, lsErrorSock
    lsConnSock = []
    lsReadSock = []
    lsWriteSock = []
    lsErrorSock = []
    mpSockCmd = {}

    #先设置监听的socket
    conn_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock1.setblocking(0)   #后面使用select多路复用，这里就直接非阻塞 socket
    conn_sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn_sock1.bind(('', 10011))
    conn_sock1.listen(5)

    lsConnSock.append(conn_sock1)

    #将conn_sock1加入可读的监控列表
    lsReadSock.append(conn_sock1)

    #监听socket设置OK之后，开始使用select来监控各个socket的情况
    #这里无限循环使用select
    while 1:
        rlist, wlist, xlist = select.select(lsReadSock, lsWriteSock, lsErrorSock, 0)

        if rlist:
            print "select : ", rlist, wlist, xlist

        #处理可读的socket列表
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

                #如果这个sock不在可写列表中，那么加入进去
                if sock not in lsWriteSock:
                    lsWriteSock.append(sock)

        #处理可写的socket列表
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
            lsWriteSock.remove(sock) #可写的内容完毕之后，要将它从可写监控列表中删除掉

    conn_sock1.close()

#专注处理rpc指令，解析接收到的消息
def process_rpc():
    pass

#专注处理数据的存储
def process_db():
    pass

def main():

    #主线程，主要处理socket链接，消息发送
    process_socket()

    #子线程1，处理rpc指令，解析接收到的消息
    rpc_threading = threading.Thread(target = process_rpc, args = ([]))

    #子线程2，处理数据存储
    db_threading = threading.Thread(target = process_db, args = ([]))

    rpc_threading.start()
    db_threading.start()

    rpc_threading.join()
    db_threading.join()

    sys.exit(-1)

if __name__ == "__main__":
    main()
