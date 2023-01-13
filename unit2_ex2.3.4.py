# exercise 2.3.4 from unit 2
'''
A client connected to the echo server and sent him the sentence "?May I help you"
In response, he received only the word "May" from the server.
What does the code of that client look like? Complete the missing part
of the plan (highlighted with a marker).

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8820))
s.send("May I help you?".encode())

print(_________________.decode())

'''

# Answer: s.recv(3)
