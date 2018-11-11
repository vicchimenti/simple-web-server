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




# establish working directory
try :
    server_home = os.getcwd()
except NameError :
    error_message = "ERROR Failed to Get Current Working Directory"
    print (error_message)
    sys.exit ("Exiting Program")

# get the hostname
try :
    host = socket.gethostname()
except AttributeError :
    error_message = "ERROR Failed to Get Hostname"
    print (error_message)
    sys.exit ("Exiting Program")

# get the host IP number
try :
    host_ip = socket.gethostbyname(host)
except AttributeError :
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
except ConnectionError :
    error_message = "ERROR Establishing a Socket"
    print (error_message)
    sys.exit ("Exiting Program")

# bind the socket to the port
try :
    sock.bind ((host, port))
except ConnectionError :
    error_message = "ERROR Binding the Host and Port"
    print (error_message)
    sys.exit ("Exiting Program")

# set socket to listen
try :
    sock.listen (maximum_queue)
except ConnectionError :
    error_message = "ERROR Opening a Listening Socket"
    print (error_message)
    sys.exit ("Exiting Program")

# print confirmation of listening socket
print ("Listening for Client on Port Number : " + user_input)




# open client sockets and exchange messages
while True :

    # reset working directory each iteration
    cwd = server_home

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
        except ConnectionError :
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
            # if request is approved method then begin processing
            if x != -1 :
                try :
                    get_request, path_protocol = \
                        client_message.split(client_method, 2)
                except IndexError :
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
                    except IndexError :
                        error_message = "ERROR Unable to Strip Protocol"
                        status = "400 Bad Request"
                        print (status + " : " + error_message)
                        EXIT_SOCKET = 4
                else :
                    error_message = "ERROR Not a Valid HTTP Request"
                    status = "400 Bad Request"
                    print (status + " : " + error_message)
                    EXIT_SOCKET = 4



                # proceed when exit socket is not active
                if EXIT_SOCKET == 0 :

                    # initialize the file string
                    requested_file = ""

                    # requested path is empty
                    if path == SINGLE_SLASH :
                        # empty path provided
                        path = cwd + WEB_ROOT
                        print ("absolute path if :" + path)

                        # update the working directory
                        try :
                            os.chdir(path)
                            print(os.getcwd())
                        except FileNotFoundError :
                            error_message = "ERROR Path Not Found"
                            status = "404 Not Found"
                            print (status + " : " + error_message)

                        # open the file and assign to a string
                        try :
                            with open(DEFAULT_FILE, 'r') as file:
                                requested_file = file.read()
                            status = "200 OK"
                        except filename :
                            error_message = "ERROR Reading Default File"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)
                        except UnicodeError :
                            error_message = "ERROR Decoding Data"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)

                    # requested path contains a directory
                    else :
                        # client provided path
                        print ("path else:" + path)
                        path = WEB_ROOT + path
                        print ("web_root + path :" + path)
                        path = cwd + path
                        print ("relative path :" + path)

                        # split the path from the requested file
                        try :
                            path, file_name = path.rsplit(SINGLE_SLASH, 1)
                            print ("absolute path else :" + path)
                        except IndexError :
                            error_message = "ERROR Spliting Filename from Path"
                            status = "400 Bad Request"
                            print (status + " : " + error_message)

                        # strip the file name of any trailing whitespace
                        try:
                            file_name = file_name.rstrip()
                            print ("file_name :" + file_name)
                        except IndexError :
                            error_message = \
                                "ERROR Striping Whitespace from Filename"
                            status = "400 Bad Request"
                            print (status + " : " + error_message)

                        # change to requested directory
                        try :
                            os.chdir(path)
                            print(os.getcwd())
                        except FileNotFoundError :
                            error_message = "ERROR Path Not Found"
                            status = "404 Not Found"
                            print (status + " : " + error_message)

                        # open the file and assign to a string
                        try :
                            with open(file_name, 'r') as file:
                                requested_file = file.read()
                            status = "200 OK"
                        except filename :
                            error_message = "ERROR Reading Requested File"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)
                        except UnicodeError :
                            error_message = "ERROR Decoding Data"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)




    # prep results for delivery
    print ("error message : " + error_message)
    print ("status : " + status)
    print ("path : " + path)
    try :
        status += NEW_LINE
        error_message += END_HEADER
        requested_file += NEW_LINE
        requested_file = status + error_message + requested_file
    except TypeError :
        error_message = "ERROR Can't Concatenate Bytes and Strings\r\n\r\n"
        status = "500 Internal Server Error\r\n"
        requested_file = status + error_message
        print (status + " : " + error_message)
    print ("requested_file : " + requested_file)
    # return results to client
    try :
        clientSock.sendall(requested_file.encode(charset))
    except OSError :
        print ("ERROR Sending Requested File")
        sys.exit ("Exiting Program")




    # Close the Client Socket
    clientSock.close()
    print ("Listening for Next Client on Port Number : " + user_input)






sys.exit()                      # Exit the Program
