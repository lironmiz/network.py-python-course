import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("127.0.0.1", 12345))

s.listen(1)

print("Server listening for incoming connections...")

while True:
    c, addr = s.accept()
    print("Connection received from", addr)

    message = c.recv(1024).decode()
    print("Received message:", message)

    modified_message = message.upper() + "!!!"

    c.send(modified_message.encode())
    c.close()
