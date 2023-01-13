# exercise 2.4.4 from unit 2
'''
After taking the network.py course, Alice and Bob want to demonstrate the extensive knowledge they have gained in the course, and want to communicate using sockets.
For this purpose, Alice decided that she would open a server, to which Bob would send the messages he wanted to deliver to her. Here is the code that Alice wrote, for creating the server.
Unfortunately, when Alice ran the attached code, she received the following error:

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 32548)
sock.listen(10)
while True:
print('waiting for a connection')
connection, client_address = sock.accept()
print("received a new connection")

Traceback (most recent call last):
File "C:/Users/exercises/Server.py", line 8, in <module>
sock.listen(10)
OSError: [WinError 10022] An invalid argument was supplied

What mistake did Alice make in writing the server?

'''

# Answer: Alice forgot to bind

