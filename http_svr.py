# Vic Chimenti
# CPSC 5510 p1b
# http_svr.py
# A Simple Web Server in Python3
# Created           10/30/2018
# Last Modified     10/30/2018
# /usr/bin/python3

import socket

HOST = '127.0.0.1'  # Default localhost
PORT = 10100        # Default Port - Assigned Range is 10100 - 10109


# open socket connection for TCP stream and listen
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    # echo response
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
