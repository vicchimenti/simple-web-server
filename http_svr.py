# Vic Chimenti
# CPSC 5510 p1b
# http_svr.py
# A Simple Web Server in Python3
# Created           10/30/2018
# Last Modified     10/30/2018
# /usr/bin/python3




import socket
import sys




# Function to reverse a string
def reverse(string):
    string = string[::-1]
    return string




HOST = '127.0.0.1'          # Default localhost
PORT = 10100                # Default Port - Assigned Range is 10100 - 10109
user_input = sys.argv[1]    # User Defined Port Number


# open socket connection for TCP stream and listen
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    client, address = sock.accept()

    # echo response
    with client:
        print('Connection Established With: ', address)
        while True:
            message = client.recv(65536)
            if not message:
                break
        response = (reverse(message))
        client.sendall(response)


client.close()              # Close the Client Socket
sys.exit()                  # Exit the Program
