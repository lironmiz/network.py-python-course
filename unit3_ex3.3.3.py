# exercise 3.3.3 from unit 3
'''
You are interested in establishing a UDP socket and sending the strings "Hello" to
the server whose IP address is 1.2.3.4 and port 53. There is no need to receive information
back. How will you do this?
'''

# Answer: 
import socket

SERVER_IP = "1.2.3.4"
PORT = 53

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket. sendto( "Hello".encode(), ( SERVER_IP, PORT))

my_socket.close()
