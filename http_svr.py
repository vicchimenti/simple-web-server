# Vic Chimenti
# CPSC 5510 p1b
# http_svr.py
# A Simple Web Server in Python3
# Created           10/30/2018
# Last Modified     11/3/2018
# /usr/bin/python3




import socket
import sys




# Reverse a String
def reverse(string):
    string = string[::-1]
    return string

# Function to acquire and display hostname / IP address
def get_host_name_IP():
    try:
        host = socket.gethostname()
        host_ip = socket.gethostbyname(host)
        print("Hostname :  ",host)
        print("IP : ",host_ip)
    except:
        print("Unable to get Hostname and IP")





# set defaults
host_ip = '127.0.0.1'           # Default localhost IP address
port = 10109                    # Default Port - Assigned Range is 10100 - 10109
maximum_queue = 1               # Serve Only One Client at a Time
get_host_name_IP()              # Identify Domain and IP on current machine



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
try :
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
except sys.OSError as e :
    print ("ERROR Creating Server Socket : " + e)

sock.bind ((host_ip, port))
sock.listen (maximum_queue)
print ("Listening for Client on Port Number : " + user_input)


(client, address) = sock.accept()
print('Connection Established With: ' + address)


# receive request
while True:
    message = clientSock.recv(65536)
    if not message:
        break


response = (reverse(message))
clientSock.sendall(response)




clientSock.close()              # Close the Client Socket
sys.exit()                      # Exit the Program
