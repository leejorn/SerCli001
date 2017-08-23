# -*- coding: utf-8 -*-

import threading
import recv_logic, send_logic, rpc_logic, db_logic

def main():
    recv_threading = threading.Thread(target = recv_logic.process_recv, args = ( [] ))
    send_threading = threading.Thread(target = send_logic.process_send, args = ( [] ))
    rpc_threading = threading.Thread(target = rpc_logic.process_rpc, args = ( [] ))
    db_threading = threading.Thread(target = db_logic.process_db, args = ( [] ))

    recv_threading.start()
    send_threading.start()
    rpc_threading.start()
    db_threading.start()

    recv_threading.join()
    send_threading.join()
    rpc_threading.join()
    db_threading.join()

    exit(1)

if __name__ == "__main__":
    main()
