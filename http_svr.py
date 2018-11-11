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




# set constants
END_HEADER = "\r\n\r\n"         # header - body delimiter
NEW_LINE = "\r\n"               # newline delimiter
SINGLE_SLASH = "/"              # single slash delimiter
DEFAULT_PATH = "/web_root/"
WEB_ROOT = "/web_root"
DEFAULT_FILE = "index.html"
EXIT_SOCKET = 0
MAL_SET = "/../"




# set defaults
port = 10109                    # Default Port - Assigned Range is 10100 - 10109
maximum_queue = 1               # Serve Only One Client at a Time
charset = "UTF-8"               # default encoding protocol
client_method = "GET"           # acceptable client method
client_protocol = "HTTP/1.1"    # acceptable client protocol
error_message = NEW_LINE        # default error message for response header





# get the hostname
try :
    host = socket.gethostname()
except OSError :
    error_message = "ERROR Failed to Get Hostname"
    print (error_message)
    sys.exit ("Exiting Program")

# get the host IP number
try :
    host_ip = socket.gethostbyname(host)
except OSError :
    error_message = "ERROR Failed to Get Host IP Number"
    print (error_message)
    sys.exit ("Exiting Program")




# get user defined port number from the command line
try :
    user_input = sys.argv[1]
except IndexError :
    error_message = "ERROR No Valid Command Line Input"
    print (error_message)
    sys.exit ("Exiting Program")
except KeyError :
    error_message = "ERROR Invalid Command Line Entry"
    print (error_message)
    sys.exit ("Exiting Program")

# convert input to port number
try :
    port = int (user_input)
except ValueError :
    error_message = "ERROR Command Line Entry is Not an Integer"
    print (error_message)
    sys.exit ("Exiting Program")




# open socket connection for TCP stream
try :
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
except OSError :
    error_message = "ERROR Establishing a Socket"
    print (error_message)
    sys.exit ("Exiting Program")

# bind the socket to the port
try :
    sock.bind ((host, port))
except OSError :
    error_message = "ERROR Binding the Host and Port"
    print (error_message)
    sys.exit ("Exiting Program")

# set socket to listen
try :
    sock.listen (maximum_queue)
except OSError :
    error_message = "ERROR Opening a Listening Socket"
    print (error_message)
    sys.exit ("Exiting Program")

# print confirmation of listening socket
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
        error_message = "ERROR Unable to Connect with Client"
        status = "500 Internal Server Error"
        print (status + " : " + error_message)
        EXIT_SOCKET = 1

    # proceed when exit socket is not active
    if EXIT_SOCKET == 0 :

        # initialize message receive string
        client_message = ""

        # receive request
        try :
            while True :
                message = clientSock.recv (65536)
                client_message += message.decode (charset)
                x = client_message.find(END_HEADER)
                if x != -1 : break
        except OSError :
                error_message = "ERROR Receiving Client Message"
                status = "500 Internal Error"
                print (status + " : " + error_message)
                EXIT_SOCKET = 2



        # proceed when exit socket is not active
        if EXIT_SOCKET == 0 :

            # Display the Client Request
            print ("Client Request :\n" + client_message)

            # parse and process client request
            x = client_message.find (client_method)
            # if request is approved request method then begin processing
            if x != -1 :
                try :
                    get_request, path_protocol = \
                        client_message.split(client_method, 2)
                except OSError :
                    error_message = "ERROR Unable to Strip Request Type"
                    status = "501 Not Implemented"
                    print (status + " : " + error_message)
                    EXIT_SOCKET = 3
            else :
                error_message = "ERROR Invalid Request Type"
                status = "501 Not Implemented"
                print (status + " : " + error_message)
                EXIT_SOCKET = 3


            # proceed when exit socket is not active
            if EXIT_SOCKET == 0 :

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
                # initialize the file string
                requested_file = ""
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
    requested_file += NEW_LINE
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
