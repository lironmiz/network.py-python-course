# exercise 3.3.4 from unit 3
'''
Find the bug in the following code:

import socket

SERVER_IP = "1.2.3.4"
PORT = 53

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.send("Hello".encode(), (SERVER_IP, PORT))
my_socket.close()

'''

# Answer: Using send and not sendto
