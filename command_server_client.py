import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect(("127.0.0.1", 1234))

while True:
    # Send request to the server
    request = input("Enter a request (NAME, TIME, RAND, Quit): ")
    s.send(request.encode())

    # Receive response from the server
    response = s.recv(1024).decode()
    print("Received response:", response)

    if request == "Quit":
        s.close()
        break
