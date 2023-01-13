# exercise 2.3.3 from unit 2
'''
You want to establish a TCP socket and send the strings "Hello" to the server whose IP address is 1.2.3.4 and port 80. There is no need to receive information back. Find the bug in the code

client_tcp.py
import socket

SERVER_IP = "1.2.3.4"
PORT = 80

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((SERVER_IP))
my_socket.send("hello".encode())
my_socket.close()
'''

# Answer: The server reference does not include a port

