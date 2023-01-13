import socket

# Server IP and port
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Get user input
    message = input("Enter a message to send to the server (EXIT to quit): ")

    # Send the message to the server
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    # Check if the message is "EXIT"
    if message == "EXIT":
        print("Closing socket...")
        client_socket.close()
        break
