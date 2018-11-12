# Vic Chimenti
# CPSC 5510 p1b
# http_svr.py
# A Simple Web Server in Python3
# Created           10/30/2018
# Last Modified     11/11/2018
# /usr/local/python3/bin/python3




import socket       # TCP Socket Operations
import sys          # System Calls
import os           # File and Directory Information
import datetime     # System Time




# *****   set constants for grammar   ***
END_HEADER = "\r\n\r\n"                 # header - body delimiter
NEW_LINE = "\r\n"                       # newline delimiter
SINGLE_SLASH = "/"                      # single slash delimiter
SEMI_COLON = ";"                        # semicolon delimiter
COLON = ":"                             # colon delimiter
WHITE_SPACE = " "                       # single whitespace




#  *****   set constants for building and formatting the response header   ***
LAST_MODIFIED_FIELD = "Last-Modified"   # contains date of last modification
CONNECTION_FIELD = "Connection"         # contains server connection status
LENGTH_FIELD = "Content-Length"         # contains length of http response
CONTENT_FIELD = "Content-Type"          # contains the file type
CHARSET_FIELD = "charset="              # contains the decoding protocol
DATE_FIELD = "Date"                     # contains the system date
TEXT_MATCH = ".html"                    # matches html file type
PNG_MATCH = ".png"                      # matches png file type
JPG_MATCH = ".jpg"                      # matches jpg file type
JPEG_MATCH = ".jpeg"                    # matches jpeg file type
TEXT_TYPE = "text/html"                 # http text message type
PNG_TYPE = "image/png"                  # http png message type
JPG_TYPE = "image/jpeg"                 # http jpg message type
JPEG_TYPE = "image/jpeg"                # http jpeg message type
HEADER_SIZE = 20                        # max header size




# *****   set constants for request parsing   ***
CLIENT_PROTOCOL = "HTTP/1.1"            # acceptable client protocol
DEFAULT_FILE_TYPE = TEXT_MATCH          # when no file type is indicated
DEFAULT_FILE = "index.html"             # when no path is provided
WEB_ROOT = "/web_root"                  # for internal path routing
MAL_SET = "/../"                        # malware delimiter




# initialize default values
port = 10109                    # Default Port - Assigned Range is 10100 - 10109
maximum_queue = 1               # Serve Only One Client at a Time
charset = "UTF-8"               # default encoding protocol
client_method = "GET"           # acceptable client method
mime_type = TEXT_TYPE           # default to text/html
file_name = DEFAULT_FILE        # file name initializes to index.html
error_message = NEW_LINE        # default error message for response header
exit_socket = 0                 # decision tree default status




# ***************    System Set Up for Socket   ***************************** #




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

# print confirmation of active listening socket
print ("Listening for Client on Port Number : " + user_input)




# **************   open client sockets and exchange messages   *************** #



# establish client socket loop
while True :

    # reset working directory each iteration
    cwd = server_home
    connection_value = "close"
    date_value = str(datetime.datetime.now())

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
                x = path_protocol.find (CLIENT_PROTOCOL)
                # if request is in HTTP format
                if x != -1 :
                    try :
                        path = path_protocol[:x]
                        protocol = CLIENT_PROTOCOL
                        path = path.strip()
                        protocol = protocol.strip()
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

                    # requested path contains a directory
                    else :
                        # client provided path
                        path = WEB_ROOT + path
                        path = cwd + path

                        # split the path from the requested file
                        try :
                            path, file_name = path.rsplit(SINGLE_SLASH, 1)
                        except IndexError :
                            error_message = "ERROR Spliting Filename from Path"
                            status = "400 Bad Request"
                            print (status + " : " + error_message)

                        # strip the file name of any trailing whitespace
                        try:
                            file_name = file_name.rstrip()
                        except IndexError :
                            error_message = \
                                "ERROR Striping Whitespace from Filename"
                            status = "400 Bad Request"
                            print (status + " : " + error_message)

                        # change to requested directory
                        try :
                            os.chdir(path)
                        except FileNotFoundError :
                            error_message = "ERROR Path Not Found"
                            status = "404 Not Found"
                            print (status + " : " + error_message)

                        # extract the file type from the filename
                        try :
                            file_name_only, file_type = os.path.splitext(file_name)
                        except OSError :
                            error_message = "ERROR Unable to Determine FileType"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)

                        # set the mime type
                        try :
                            if file_type == TEXT_MATCH :
                                mime_type = TEXT_TYPE
                            elif file_type == PNG_MATCH :
                                mime_type = PNG_TYPE
                            elif file_type == JPG_MATCH :
                                mime_type = JPG_TYPE
                            elif file_type == JPEG_MATCH :
                                mime_type = JPEG_TYPE
                            else :
                                error_message = "ERROR Assigning MIME Type"
                                status = "500 Internal Server Error"
                                print (status + " : " + error_message)
                        except OSError :
                            error_message = "ERROR Assigning MIME Type"
                            status = "500 Internal Server Error"
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

                        # get time last modified
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
                            error_message = "ERROR Reading Requested File"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)
                        except UnicodeError :
                            error_message = "ERROR Decoding Data"
                            status = "500 Internal Server Error"
                            print (status + " : " + error_message)



    # if no errors
    if error_message == NEW_LINE :

        # prep results for delivery
        try :
            status_line =   protocol + WHITE_SPACE + status + NEW_LINE
            content_line =  CONTENT_FIELD        + COLON \
                                                + WHITE_SPACE \
                                                + mime_type \
                                                + SEMI_COLON \
                                                + WHITE_SPACE \
                                                + CHARSET_FIELD \
                                                + charset \
                                                + NEW_LINE
            date_line =     DATE_FIELD          + COLON \
                                                + WHITE_SPACE \
                                                + date_value \
                                                + NEW_LINE
            modified_line = LAST_MODIFIED_FIELD + COLON \
                                                + WHITE_SPACE \
                                                + modified_date \
                                                + NEW_LINE
            length_line =   LENGTH_FIELD        + COLON \
                                                + WHITE_SPACE \
                                                + length_str \
                                                + NEW_LINE
            connect_line =  CONNECTION_FIELD    + COLON \
                                                + WHITE_SPACE \
                                                + connection_value \
                                                + NEW_LINE
            reply_header =  status_line         + content_line \
                                                + date_line \
                                                + modified_line \
                                                + length_line \
                                                + connect_line \
                                                + END_HEADER
        except TypeError :
            error_message = "ERROR Can't Concatenate Bytes and Strings\r\n\r\n"
            status = "500 Internal Server Error\r\n"
            requested_file = status + error_message
            print (status + " : " + error_message)




        # encode header and append to requested file
        try :
            header_in_bytes = reply_header.encode(charset)
            response = header_in_bytes + requested_file
        except UnicodeError :
            error_message = "ERROR Encode Reply Header\r\n\r\n".encode(charset)
            status = "500 Internal Server Error\r\n".encode(charset)
            requested_file = status + error_message




        # return results to client
        try :
            clientSock.sendall(response)
        except OSError :
            print ("ERROR Sending Requested File")
            sys.exit ("Exiting Program")




    # return an error response
    else:
        status += NEW_LINE
        error_message += END_HEADER
        error_response = status + error_message
        # return error to client
        try :
            clientSock.sendall(error_response.encode(charset))
        except OSError :
            print ("ERROR Sending Requested File")
            sys.exit ("Exiting Program")




    # Close the Client Socket
    print ("Response Sent : Closing Client Socket")
    clientSock.close()
    print ("Listening for Next Client on Port Number : " + user_input)

# TODO :    look at last modified time
#           review error checking
#           review assignment requirements
#           move to cs2 and test with commercial browser




sys.exit()                      # Exit the Program
