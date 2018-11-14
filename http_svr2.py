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
client_method = "GET"           # acceptable client method
client_protocol = "HTTP/1.1"    # acceptable client protocol
endOf_header = "\r\n\r\n"       # header - body delimiter
END_RESPONSE = "\r\n\t\r\n\t"
new_line = "\r\n"               # newline delimiter
SINGLE_SLASH = "/"
DEFAULT_PATH = "web_root/index.html"
requested_file = ""#bytearray()
WEB_ROOT = "web_root"






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
    try :
        while True :
            message = clientSock.recv (4096)
            client_message += message.decode ('utf-8')
            x = client_message.find(endOf_header)
            if x != -1 : break
    except OSError :
        print ("ERROR Receiving Request: ")
        sys.exit ("Exiting Program")

    # *** TS Print Message
    print ("Message Received : " + client_message)




    # parse and process client request
    x = client_message.find (client_method)
    # if request is GET then truncate message
    if x != -1 :
        get_request, path_protocol = client_message.split(client_method, 2)
    else :
        status = "501 Not Implemented"
        status += endOf_header
        clientSock.sendall (status.encode ('utf-8'))
        clientSock.close()

    #if protocol is HTTP parse path from message
    x = path_protocol.find (client_protocol)
    # if request is in HTTP format
    if x != -1 :
        try :
            path = path_protocol[:x]
            path = path.lstrip()
            print ("path_holder :" + path)
        except OSError :
            sys.stderr.write("ERROR Unable to Strip Path")
            sys.exit("Exiting Program")
    else :
        status = "400 Bad Request"
        status += endOf_header
        try :
            clientSock.sendall (status.encode ('utf-8'))
            clientSock.close()
        except OSError :
            sys.stderr.write("ERROR Sending Status Code 400")
            sys.exit("Exiting Program")

    # validate requested path
    if path == '/' :
        path = DEFAULT_PATH
        try :
            with open(path, "r") as file:
                requested_file = file.read()
        except OSError :
            sys.stderr.write("ERROR Reading File")
            sys.exit("Exiting Program")
        print ("ERROR Accessing Default Path")
        status = "404 Not Found"
        status += endOf_header
        clientSock.sendall (status.encode ('utf-8'))
        clientSock.close()

    else :
        print ("path else:" + path)
        path = WEB_ROOT + path
        print ("web_root + path :" + path)
        try :
            with open(path, "r") as file:
                requested_file = file.read()
        except OSError :
            print ("ERROR Accessing Path Provided")
            status = "404 Not Found"
            status += endOf_header

            print ("status : " + status)
            clientSock.sendall (status.encode ('utf-8'))
            clientSock.close()
            sys.exit ("Exiting Program")




    # send file to client
    print ("path : " + path)
    print ("requested_file : " + requested_file)
    #delim_in_bytes = END_RESPONSE.encode('utf-8')
    requested_file += endOf_header
    try :
        clientSock.sendall(requested_file.encode('utf-8'))
    except OSError :
        print ("ERROR Sending Requested File")
        sys.exit ("Exiting Program")




    # Close the Client Socket
    clientSock.close()




sys.exit()                      # Exit the Program



                        # update the working directory
                        try :
                            os.chdir(path)
                            print(os.getcwd())
                        except FileNotFoundError :
                            error_message = "ERROR Path Not Found"
                            status = "404 Not Found"
                            print (status + " : " + error_message)

                        # get file size and convert to string
                        try :
                            file_size = os.path.getsize(file_name)
                            file_size += HEADER_SIZE
                            length_str = str(file_size)
                        except OSError :
                            error_message = "ERROR Obtaining File Size"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)

                        # get time last modified and convert to string
                        try :
                            modified_date = str(os.path.getmtime(file_name))
                        except OSError :
                            error_message = "ERROR Obtaining Modified Time"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)

                        # open the file and assign to a string
                        try :
                            with open(file_name, 'rb') as file:
                                requested_file = file.read()
                            status = "200 OK"
                        except FileNotFoundError :
                            error_message = "ERROR Reading Default File"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)
                        except UnicodeError :
                            error_message = "ERROR Decoding Data"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)
