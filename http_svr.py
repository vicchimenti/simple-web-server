# Vic Chimenti
# CPSC 5510 p1b
# http_svr.py
# A Simple Web Server in Python3
# Created           10/30/2018
# Last Modified     2/18/2019
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
error_message = NEW_LINE        # default error message for response header
path_protocol = CLIENT_PROTOCOL # default assignment : will assign within if statement
path_raw = path_protocol        # default assignment : will assign within if statement
file_type = mime_type           # default assignment : will assign within if statement
protocol = path_raw             # default assignment : will assign within if statement
modified_date = DATE_FIELD      # default assignment : will assign within if statement
length_str = ''                 # default assignment : will assign within if statement
reply_header = ''                # default assignment : will assign within if statement


# ***************    System Set Up for Socket   ***************************** #s


# establish working directory
try:
    server_home = os.getcwd()
except NameError:
    error_message = "ERROR Failed to Get Current Working Directory"
    print(error_message)
    sys.exit("Exiting Program")

# get the hostname
try:
    host = socket.gethostname()
except AttributeError:
    error_message = "ERROR Failed to Get Hostname"
    print(error_message)
    sys.exit("Exiting Program")

# get the host IP number
try:
    host_ip = socket.getaddrinfo(host, port)
except AttributeError:
    error_message = "ERROR Failed to Get Host IP Number"
    print(error_message)
    sys.exit("Exiting Program")

"""
# get user defined port number from the command line
try:
    user_input = sys.argv[1]
except IndexError:
    error_message = "ERROR No Valid Command Line Input"
    print(error_message)
    # sys.exit("Exiting Program")
except KeyError:
    error_message = "ERROR Invalid Command Line Entry"
    print(error_message)
    # sys.exit("Exiting Program")

# convert input to port number
try:
    port = int(user_input)
except ValueError:
    error_message = "ERROR Command Line Entry is Not an Integer"
    print(error_message)
    # sys.exit("Exiting Program")
"""

# open socket connection for TCP stream
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except ConnectionError:
    error_message = "ERROR Establishing a Socket"
    print(error_message)
    sys.exit("Exiting Program")

# bind the socket to the port
try:
    sock.bind((host, port))
except ConnectionError:
    error_message = "ERROR ConnectionError Binding the Host and Port"
    print(error_message)
    sys.exit("Exiting Program")
except OSError:
    error_message = "ERROR Port Already in Use"
    print(error_message)
    sys.exit("Exiting Program")

# set socket to listen
try:
    sock.listen(maximum_queue)
except ConnectionError:
    error_message = "ERROR Opening a Listening Socket"
    print(error_message)
    sys.exit("Exiting Program")

# print confirmation of active listening socket
print("Listening for Client on Port Number : " + str(port))


# **************   open client sockets and exchange messages   *************** #

# establish client socket loop
while True:

    # reset client defaults
    cwd = server_home
    exit_socket = 0
    error_message = NEW_LINE
    date_value = str(datetime.datetime.now())
    requested_file = ""

    # reset working directory each iteration
    try:
        os.chdir(cwd)
    except FileNotFoundError:
        error_message = "ERROR Path Not Found"
        status = "404 Not Found"
        exit_socket = 10

    # initialize header fields
    connection_value = "close"
    status = ""

    # connect to client
    try:
        (clientSock, address) = sock.accept()
        addr_str = str(address)
        print("Connection Established With: " + addr_str)
    except NameError:
        error_message = "Error sock.accept() did not assign values correctly"
        status = "500 Internal Server Error"
        exit_socket = 11
    except ConnectionError:
        error_message = "ERROR Unable to Connect with Client"
        status = "500 Internal Server Error"
        exit_socket = 11

    # proceed when exit socket is not active
    if exit_socket == 0:
        # initialize message receive string
        client_message = ""

        # receive request until delimiter found
        try:
            while True:
                # noinspection PyUnboundLocalVariable
                message = clientSock.recv(4096)
                client_message += message.decode(charset)
                x = client_message.find(END_HEADER)
                if x != -1:
                    break
        except ConnectionError:
                error_message = "ERROR Receiving Client Message"
                status = "500 Internal Error"
                exit_socket = 20

        # begin parsing request when exit socket is not active
        if exit_socket == 0:

            # Display the Client Request
            print("Client Request :\n" + client_message)

            # scan for malware
            x = client_message.find(MAL_SET)
            if x != -1:
                error_message = "ERROR Invalid Request Attempt"
                status = "400 Bad Request"
                exit_socket = 30

            # when no mal script present
            else:
                # parse and process client request
                x = client_message.find(client_method)
                # if request is approved method then begin processing
                if x != -1:
                    try:
                        get_request, path_protocol = \
                            client_message.split(client_method, 2)
                    except IndexError:
                        error_message = "ERROR Unable to Strip Request Type"
                        status = "501 Not Implemented"
                        exit_socket = 31
                    except NameError:
                        error_message = "ERROR client_message.split did not assign values correctly"
                        status = "501 Not Implemented"
                        exit_socket = 31

                else:
                    error_message = "ERROR Invalid Request Type"
                    status = "501 Not Implemented"
                    exit_socket = 32

            # parse the pathway from the request protocol
            if exit_socket == 0:

                # if protocol is HTTP parse path from message
                x = path_protocol.find(CLIENT_PROTOCOL)
                # if request is in HTTP format
                if x != -1:
                    try:
                        path_raw = path_protocol[:x]
                        # assign local via constant until more protocols approved
                        protocol = CLIENT_PROTOCOL
                        path_raw = path_raw.strip()
                        protocol = protocol.strip()
                    except IndexError:
                        error_message = "ERROR Unable to Strip Protocol"
                        status = "400 Bad Request"
                        exit_socket = 40
                else:
                    error_message = "ERROR Not a Valid HTTP Request"
                    status = "400 Bad Request"
                    exit_socket = 41

                # initialize the file string
                file_name = ""
                # proceed when exit socket is not active
                if exit_socket == 0:

                    # finalize the working directory
                    path = cwd + WEB_ROOT + path_raw

                    # in the case of an empty path
                    if path_raw == SINGLE_SLASH:

                        # finalize the working directory and default file
                        file_name = DEFAULT_FILE

                        # change to requested directory
                        try:
                            os.chdir(path)
                        except FileNotFoundError:
                            error_message = "ERROR Valid Path Not Found"
                            status = "404 Not Found"
                            exit_socket = 50

                    # requested path contains a directory then check for file extension
                    elif os.path.isfile(path):

                        # the path ends in a file extension so extract the path from the file
                        try:
                            path, file_name = path.rsplit(SINGLE_SLASH, 1)
                        except IndexError:
                            error_message = "ERROR Splitting Filename from Path"
                            status = "400 Bad Request"
                            exit_socket = 51

                        # strip the file name of any trailing whitespace
                        try:
                            file_name = file_name.rstrip()
                        except IndexError:
                            error_message = \
                                "ERROR Striping Whitespace from Filename"
                            status = "400 Bad Request"
                            exit_socket = 52

                        # change to requested directory
                        try:
                            os.chdir(path)
                        except FileNotFoundError:
                            error_message = "ERROR File Not Found"
                            status = "404 Not Found"
                            exit_socket = 53

                    # or else the path does not contain a filename
                    elif os.path.isdir(path):

                        # use the default file
                        file_name = DEFAULT_FILE

                        # change to requested directory
                        try:
                            os.chdir(path)
                        except FileNotFoundError:
                            error_message = "ERROR Path Not Found"
                            status = "404 Not Found"
                            exit_socket = 54

                    # or else no valid path is given
                    else:
                        error_message = "ERROR Invalid Path Requested"
                        status = "404 Not Found"
                        exit_socket = 55

                    # gather file information and store for header
                    if exit_socket == 0:

                        # extract the file type from the filename
                        try:
                            file_name_only, file_type = os.path.splitext(file_name)
                        except OSError:
                            error_message = "ERROR Unable to Determine FileType"
                            status = "500 Internal Server Error"
                            exit_socket = 60

                        # set the mime type
                        try:
                            if file_type == TEXT_MATCH:
                                mime_type = TEXT_TYPE
                            elif file_type == PNG_MATCH:
                                mime_type = PNG_TYPE
                            elif file_type == JPG_MATCH:
                                mime_type = JPG_TYPE
                            elif file_type == JPEG_MATCH:
                                mime_type = JPEG_TYPE
                            else:
                                error_message = "ERROR Assigning MIME Type"
                                status = "500 Internal Server Error"
                        except OSError:
                            error_message = "ERROR Assigning MIME Type"
                            status = "500 Internal Server Error"
                            exit_socket = 61

                        # get file size and convert to string
                        try:
                            file_size = os.path.getsize(file_name)
                            length_str = str(file_size)
                        except OSError:
                            error_message = "ERROR Obtaining File Size"
                            status = "500 Internal Server Error"
                            exit_socket = 62

                        # get time last modified
                        try:
                            md_stamp = os.path.getmtime(file_name)
                            md_obj = datetime.datetime.fromtimestamp(md_stamp)
                            modified_date = md_obj.strftime("%Y-%m-%d %H:%M:%S")
                        except OSError:
                            error_message = "ERROR Obtaining Modified Time"
                            status = "500 Internal Server Error"
                            exit_socket = 63

                        # open file and stream data
                        if exit_socket == 0:

                            # open the file and assign to a string
                            try:
                                with open(file_name, 'rb') as file:
                                    requested_file = file.read()
                                status = "200 OK"
                            except FileNotFoundError:
                                error_message = "ERROR Reading Requested File"
                                status = "500 Internal Server Error"
                                exit_socket = 70
                            except UnicodeError:
                                error_message = "ERROR Decoding Data"
                                status = "500 Internal Server Error"
                                exit_socket = 71

    #  *********************   if no errors   ******************************** #
    if error_message == NEW_LINE:

        # prep results for delivery
        try:
            status_line =   protocol + WHITE_SPACE  + status + NEW_LINE
            content_line =  CONTENT_FIELD           + COLON \
                                                    + WHITE_SPACE \
                                                    + mime_type \
                                                    + SEMI_COLON \
                                                    + WHITE_SPACE \
                                                    + CHARSET_FIELD \
                                                    + charset \
                                                    + NEW_LINE
            date_line =     DATE_FIELD              + COLON \
                                                    + WHITE_SPACE \
                                                    + date_value \
                                                    + NEW_LINE
            modified_line = LAST_MODIFIED_FIELD     + COLON \
                                                    + WHITE_SPACE \
                                                    + modified_date \
                                                    + NEW_LINE
            length_line =   LENGTH_FIELD            + COLON \
                                                    + WHITE_SPACE \
                                                    + length_str \
                                                    + NEW_LINE
            connect_line =  CONNECTION_FIELD        + COLON \
                                                    + WHITE_SPACE \
                                                    + connection_value \
                                                    + NEW_LINE
            reply_header =  status_line             + content_line \
                                                    + date_line \
                                                    + modified_line \
                                                    + length_line \
                                                    + connect_line \
                                                    + END_HEADER
        except TypeError:
            error_message = "ERROR Can't Concatenate Bytes and Strings\r\n\r\n".encode(charset)
            status = "500 Internal Server Error\r\n".encode(charset)
            response = status + error_message
            print(status.decode(charset) + " : " + error_message.decode(charset))

        # encode header and append to requested file for server response
        try:
            header_in_bytes = reply_header.encode(charset)
            response = header_in_bytes + requested_file
        except UnicodeError:
            error_message = "ERROR Encode Reply Header\r\n\r\n".encode(charset)
            status = "500 Internal Server Error\r\n".encode(charset)
            response = status + error_message
            print(status.decode(charset) + " : " + error_message.decode(charset))

        # return results to client
        print(status)
        try:
            clientSock.sendall(response)
        except OSError:
            print("ERROR Sending Requested File")
            sys.exit("Exiting Program")

    # return an error response
    else:
        status += END_HEADER
        exit_code = str(exit_socket)
        error_response = status
        print(error_response + error_message + " : " + exit_code)
        # return error to client
        try:
            clientSock.sendall(error_response.encode(charset))
        except OSError:
            print("ERROR Sending Requested File")
            sys.exit("Exiting Program")

    # Close the Client Socket
    print("Response Sent : Closing Client Socket")
    clientSock.close()
    print("Listening for Next Client on Port Number : " + str(port))


# Close the Listening Socket
# noinspection PyUnreachableCode
sock.close()
# Exit the Program
sys.exit()
