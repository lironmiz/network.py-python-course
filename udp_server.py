import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind((SERVER_IP, SERVER_PORT))

print("Server is listening...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode()
    print(f"Received message from {client_address}: {message}")

    if message == "EXIT":
        print("Closing socket...")
        server_socket.close()
        break
