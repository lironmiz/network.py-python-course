import socket
import time
import random

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
s.bind(("127.0.0.1", 1234))

# Listen for incoming connectionsNAM
s.listen(1)

print("Server listening for incoming connections...")

while True:
    # Wait for a connection
    c, addr = s.accept()
    print("Connection received from", addr)

    # Continue communication as long as the client does not send "Quit"
    while True:
        # Receive request from the client
        request = c.recv(1024).decode()
        print("Received request:", request)

        # Check the request and send the appropriate response
        if request == "NAME":
            response = "Server name: liron_server"
        elif request == "TIME":
            response = "Current time: " + time.ctime()
        elif request == "RAND":
            response = "Random number: " + str(random.randint(1, 10))
        elif request == "Quit":
            response = "Disconnecting..."
            c.send(response.encode())
            c.close()
            break
        else:
            response = "Invalid request"

        # Send the response to the client
        c.send(response.encode())

        if request == "Quit":
            break
