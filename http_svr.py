# Vic Chimenti
# CPSC 5510 p1b
# http_svr.py
# A Simple Web Server in Python3
# Created           10/30/2018
# Last Modified     11/6/2018
# /usr/local/python3/bin/python3




import socket
import sys




# set defaults
port = 10109                    # Default Port - Assigned Range is 10100 - 10109
maximum_queue = 1               # Serve Only One Client at a Time
full_message = ""               # string to collect decoded client message
client_method = "GET"           # acceptable client method
client_protocol = "HTTP/1.1"    # acceptable client protocol





# get the hostname
try :
    host = socket.gethostname()
except OSError as e :
    print ("ERROR Failed to Get Hostname : " + e)
    sys.exit ("Exiting Program")

# get the host IP number
try :
    host_ip = socket.gethostbyname(host)
except OSError as e :
    print ("ERROR Failed to Get Host IP Number : " + e)
    sys.exit ("Exiting Program")

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
    print ("Connection Established With: " + addr_str)


    # receive request
    while True :
        message = clientSock.recv (4096)
        full_message += message.decode ('utf-8')
        if not message : break


    # parse message for path
    print ("Message Received : " + full_message)


    # **** TS Echo ****
    clientSock.sendall(full_message.encode ('utf-8'))
    print ("Message Sent : " + full_message)


    # respond to request
    # clientSock.sendfile("/web_root/index.html")


    # Close the Client Socket
    clientSock.close()




# *** TS *** stall program end
admin_response = input ("Would you like to accept another client? : y/n: ")
print (admin_response)




sys.exit()                      # Exit the Program












#def send_file(path, sock):
#    with open(path, "rb") as file:
        # First read file into memory
#        content = file.read()
        # Now calculate size and convert it into 8-byte long bytes sequence
#        size = struct.pack("<Q", len(content))
        # Send the file size
#        sock.send(size)
        # Send the file
#        sock.send(content)
