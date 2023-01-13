# exercise 2.4.5 from unit 2
'''
Here is server code (server.py) and client code (client.py). The client wants to send the word hello to the server.

Server code:

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10095)
sock.bind(server_address)
sock.listen(1)
while True:
  print('waiting for a connection')
  connection, client_address = sock.accept()
  print("received a new connection")

Client code: 

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10095)
sock.connect(server_address)
sock.send("hello".encode())

The server code runs and then the client code. The server did not receive the hello message,
but the client claims that it did send it. What is the reason?

'''

# Answer: The server did not use the recv method to read
