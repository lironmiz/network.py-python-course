import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 12345))

message = input("Enter a message to send to the server: ")
s.send(message.encode())

modified_message = s.recv(1024).decode()
print("Received modified message:", modified_message)

s.close()
