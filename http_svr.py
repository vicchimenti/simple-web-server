# Vic Chimenti
# CPSC 5510 p1b
# http_svr.py
# A Simple Web Server in Python3
# Created           10/30/2018
# Last Modified     11/5/2018
# /usr/local/python3/bin/python3




import socket
import sys



# Reverse a String
def reverse(string):
    string = string[::-1]
    return string




# set defaults
port = 10109            # Default Port - Assigned Range is 10100 - 10109
maximum_queue = 1       # Serve Only One Client at a Time




# get the hostname
try :
    host = socket.gethostname()
except OSError as e :
    print ("ERROR Failed to Get Hostname : " + e)
    sys.exit("Exiting Program")

# get the host IP number
try :
    host_ip = socket.gethostbyname(host)
except OSError as e :
    print ("ERROR Failed to Get Host IP Number : " + e)
    sys.exit("Exiting Program")

# *************TS OUTPUT *****************
print ("Hostname :  " + host)
print ("IP : ", host_ip)




# get user defined port number from the command line
try :
    user_input = sys.argv[1]
except sys.IndexError as e :
    print ("ERROR No Valid Command Line Input : " + e)
    sys.exit ("Exiting Program")
except sys.KeyError as e :
    print ("ERROR Invalid Command Line Entry : " + e)
    sys.exit ("Exiting Program")



# convert input to port number
try :
    port = int (user_input)
except sys.ValueError as e :
    print ("ERROR Not an Integer : " + e)
    sys.exit ("Exiting Program")




# open socket connection for TCP stream and listen
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.bind ((host, port))
sock.listen (maximum_queue)
print ("Listening for Client on Port Number : " + user_input)



while True :
    (clientSock, address) = sock.accept()
    addr_str = str (address)
    print('Connection Established With: ' + addr_str)




    # receive request
    while True :
        message = clientSock.recv (4096)
        if not message : break



    # parse message for path
    message = message.decode('utf-8')
    print ("Message : " + message)


    # TS ****
    reverse(message)
    clientSock.sendall(message.encode('utf-8'))
    
    # respond to request
    # client.sendfile()
    # Close the Client Socket
    clientSock.close()




# *** TS *** stall program end
admin_response = input ("Would you like to accept another client? : y/n: ")
print (admin_response)




sys.exit()                      # Exit the Program
