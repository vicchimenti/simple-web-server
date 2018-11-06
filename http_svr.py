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
client_method = "GET"           # acceptable client method
client_protocol = "HTTP/1.1"    # acceptable client protocol
endOf_header = "\r\n\r\n"       # header - body delimiter





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

    # string to collect decoded client message
    client_message = ""
    status = ""

    # receive request
    while True :
        message = clientSock.recv (4096)
        client_message += message.decode ('utf-8')
        if not message : break


    # *** TS Print Message
    print ("Message Received : " + full_message)

    # parse request for GET
    x = client_message.find (client_method)

    # if request is GET then truncate message
    if x != -1 :
        #path_protocol = full_message[x+1:]
        client_message.replace (client_method, "")
    else :
        status = "501 Not Implemented – the request method was not GET"
        clientSock.sendall (status.encode ('utf-8'))
        clientSock.close()
        break

    #if protocol is HTTP parse path from message
    x = client_message.find (client_protocol)

    # if request is in HTTP format
    if x != -1 :
        path = client_message[:x]
    else :
        status = "400 Bad Request – the request is not a properly formed HTTP request"
        clientSock.sendall (status.encode ('utf-8'))
        clientSock.close()
        break


    # **** TS Echo Path ****
    clientSock.sendall(path.encode ('utf-8'))
    print ("Message Sent : " + path)

    # respond to request
    # feed file contents into a string before sending body
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
