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
DEFAULT_PATH = "/web_root/"
WEB_ROOT = "/web_root"
DEFAULT_FILE = "index.html"






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
    requested_file = ""
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
            sys.stderr.write("ERROR Receiving Client Message : ")
            status = "500 Internal Error"
            status += endOf_header

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
            status += endOf_header
    else :
        status = "501 Not Implemented"
        status += endOf_header




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
            status += endOf_header
    else :
        status = "400 Bad Request"
        status += endOf_header


    # get the current working directory
    cwd = os.getcwd()
    # validate requested path
    if path == '/' :
        # empty path provided
        path = DEFAULT_PATH
        # update the working directory
        os.chdir(path)
        try :
            with open(DEFAULT_FILE, "r") as file:
                requested_file = file.read()
        except OSError :
            sys.stderr.write("ERROR Reading Default File : ")
            status = "404 Not Found"
            status += endOf_header

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
            status += endOf_header
        try :
            with open(file_name, 'r') as file:
                requested_file = file.read()
            status = "200 OK"
            status += endOf_header
        except OSError :
            print ("ERROR Reading Requested File")
            status = "500 Internal Server Error"
            status += endOf_header







    # send file to client
    print ("status : " + status)
    print ("path : " + path)
    requested_file += new_line
    requested_file = status + requested_file
    print ("requested_file : " + requested_file)

    try :
        clientSock.sendall(requested_file.encode('utf-8'))
    except OSError :
        print ("ERROR Sending Requested File")
        sys.exit ("Exiting Program")




    # Close the Client Socket
    clientSock.close()
    print ("Listening for Next Client on Port Number : " + user_input)




sys.exit()                      # Exit the Program
