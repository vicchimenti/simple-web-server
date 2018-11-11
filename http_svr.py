# Vic Chimenti
# CPSC 5510 p1b
# http_svr.py
# A Simple Web Server in Python3
# Created           10/30/2018
# Last Modified     11/10/2018
# /usr/local/python3/bin/python3




import socket
import sys
import os                       # file and directory information




# set defaults
port = 10109                    # Default Port - Assigned Range is 10100 - 10109
maximum_queue = 1               # Serve Only One Client at a Time
charset = "UTF-8"               # default encoding protocol
client_method = "GET"           # acceptable client method
client_protocol = "HTTP/1.1"    # acceptable client protocol
END_HEADER = "\r\n\r\n"         # header - body delimiter
new_line = "\r\n"               # newline delimiter
SINGLE_SLASH = "/"              # single slash delimiter
DEFAULT_PATH = "/web_root/"
WEB_ROOT = "/web_root"
DEFAULT_FILE = "index.html"
EXIT_SOCKET = 0







# get the hostname
try :
    host = socket.gethostname()
except OSError :
    print ("ERROR Failed to Get Hostname")
    sys.exit ("Exiting Program")

# get the host IP number
try :
    host_ip = socket.gethostbyname(host)
except OSError :
    print ("ERROR Failed to Get Host IP Number")
    sys.exit ("Exiting Program")




# get user defined port number from the command line
try :
    user_input = sys.argv[1]
except sys.IndexError :
    print ("ERROR No Valid Command Line Input")
    sys.exit ("Exiting Program")
except sys.KeyError :
    print ("ERROR Invalid Command Line Entry")
    sys.exit ("Exiting Program")

# convert input to port number
try :
    port = int (user_input)
except sys.ValueError as e :
    print ("ERROR Command Line Entry is Not an Integer")
    sys.exit ("Exiting Program")




# open socket connection for TCP stream and listen
try :
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
except OSError :
    print ("ERROR Establishing a Socket")
    sys.exit ("Exiting Program")
try :
    sock.bind ((host, port))
except OSError :
    print ("ERROR Binding the Host and Port")
    sys.exit ("Exiting Program")
try :
    sock.listen (maximum_queue)
except OSError :
    print ("ERROR Opening a Listening Socket")
    sys.exit ("Exiting Program")
print ("Listening for Client on Port Number : " + user_input)




# open client sockets and exchange messages
while True :

    # initialize header status field
    status = ""

    try :
        (clientSock, address) = sock.accept()
        addr_str = str (address)
        print ("Connection Established With: " + addr_str)
    except ConnectionError :
        print ("ERROR Unable to Connect with Client")
        status = "500 Internal Server Error"
        EXIT_SOCKET = 1

    # proceed when exit socket is not active
    if EXIT_SOCKET == 0 :

        # initialize header status field
        requested_file = ""
        client_message = ""

        # receive request
        try :
            while True :
                message = clientSock.recv (65536)
                client_message += message.decode (charset)
                x = client_message.find(END_HEADER)
                if x != -1 : break
        except OSError :
                print ("ERROR Receiving Client Message : ")
                status = "500 Internal Error"
                status += END_HEADER

        # *** TS Print Message
        print ("Message Received : " + client_message)




        # parse and process client request
        x = client_message.find (client_method)
        # if request is GET then truncate message
        if x != -1 :
            try :
                get_request, path_protocol = client_message.split(client_method, 2)
            except OSError :
                sys.stderr.write("ERROR Unable to Strip Request Type : ")
                status = "501 Not Implemented"
                status += END_HEADER
        else :
            status = "501 Not Implemented"
            status += END_HEADER




        #if protocol is HTTP parse path from message
        x = path_protocol.find (client_protocol)
        # if request is in HTTP format
        if x != -1 :
            try :
                path = path_protocol[:x]
                path = path.strip()
                print ("path_holder :" + path)
            except OSError :
                sys.stderr.write("ERROR Unable to Strip Protocol : ")
                status = "400 Bad Request"
                status += END_HEADER
        else :
            status = "400 Bad Request"
            status += END_HEADER


        # get the current working directory
        cwd = os.getcwd()
        # validate requested path
        if path == SINGLE_SLASH :
            # empty path provided
            path = DEFAULT_PATH
            path = cwd + path
            # update the working directory
            os.chdir(path)
            try :
                with open(DEFAULT_FILE, 'rb') as file:
                    requested_file = file.read()
            except OSError :
                sys.stderr.write("ERROR Reading Default File : ")
                status = "404 Not Found"
                status += END_HEADER

        else :
            # client provided path
            print ("path else:" + path)
            path = WEB_ROOT + path
            print ("web_root + path :" + path)
            path = cwd + path
            print ("relative path :" + path)
            path, file_name = path.rsplit(SINGLE_SLASH, 1)
            print ("absolute path :" + path)
            file_name = file_name.rstrip()
            print ("file_name :" + file_name)
            try :
                os.chdir(path)
                print(os.getcwd())
            except FileNotFoundError :
                print ("ERROR Path Not Found")
                status = "404 Not Found"
                status += END_HEADER
            try :
                with open(file_name, 'rb') as file:
                    requested_file = file.read()
                status = "200 OK"
                status += END_HEADER
            except OSError :
                print ("ERROR Reading Requested File")
                status = "500 Internal Server Error"
                status += END_HEADER



    # send file to client
    print ("status : " + status)
    print ("path : " + path)
    requested_file += new_line
    requested_file = status + requested_file
    print ("requested_file : " + requested_file)

    try :
        clientSock.sendall(requested_file.encode(charset))
    except OSError :
        print ("ERROR Sending Requested File")
        sys.exit ("Exiting Program")




        # Close the Client Socket
        clientSock.close()
        print ("Listening for Next Client on Port Number : " + user_input)






sys.exit()                      # Exit the Program
